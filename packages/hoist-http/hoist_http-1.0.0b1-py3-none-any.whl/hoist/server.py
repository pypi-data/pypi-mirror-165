import inspect
import logging
import socket
from contextlib import suppress
from secrets import choice, compare_digest
from string import ascii_letters
from threading import Thread
from traceback import format_exception
from typing import (
    TYPE_CHECKING, Any, List, Optional, Sequence, Type, TypeVar, get_type_hints
)

import uvicorn
from rich import box
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocket, WebSocketDisconnect
from versions import Version, parse_version
from yarl import URL

from .__about__ import __version__
from ._errors import (
    BAD_VERSION, INVALID_ACTION, INVALID_CONTENT, LOGIN_FAILED, SERVER_ERROR,
    UNKNOWN_OPERATION, UNSUPPORTED_OPERATION
)
from ._html import HTML
from ._logging import hlog, log
from ._messages import (
    LISTENER_CLOSE, LISTENER_OPEN, NEW_MESSAGE, SINGLE_NEW_MESSAGE,
    BaseMessagable, MessageListener
)
from ._operations import BASE_OPERATIONS, OperatorParam
from ._schema import invalid_payload, verify_schema
from ._socket import ClientError, Socket, Status, make_client, make_client_msg
from ._typing import (
    JSONLike, LoginFunc, MessageListeners, OperationData, Operations, Operator,
    Payload, Schema, VersionLike
)
from ._uvicorn import UvicornServer
from .exceptions import (
    AlreadyInUseError, CloseSocket, SchemaValidationError,
    ServerNotStartedError
)
from .message import Message, PendingMessage

if TYPE_CHECKING:
    from _typeshed import SupportsLenAndGetItem

logging.getLogger("uvicorn.error").disabled = True
logging.getLogger("uvicorn.access").disabled = True

__all__ = ("Server",)

T = TypeVar("T")
_CONSOLE = Console()
print_exc = _CONSOLE.print_exception


async def _base_login(server: "Server", sent_token: str) -> bool:
    """Default login function used by servers."""
    return compare_digest(server.token, sent_token)


class _SocketMessageTransport(BaseMessagable):
    """Connection class for wrapping message objects."""

    def __init__(
        self,
        ws: Socket,
        server: "Server",
        id: Optional[int],
        event_message: str = NEW_MESSAGE,
    ) -> None:
        self._ws = ws
        self._server = server
        self._message = event_message
        self._id = id

    async def message(
        self,
        msg: str,
        data: Optional[Payload] = None,
        replying: Optional[Message] = None,
        listeners: Optional[MessageListeners] = None,
    ) -> Message:
        """Send a message to the client."""
        d = data or {}
        reply = replying.to_dict() if replying else None

        obj = await self._server.new_message(
            self,
            msg,
            d,
            reply,
        )
        obj.message_listeners = listeners or {}

        await self._ws.success(
            self._id,
            message=self._message,
            payload={
                "message": msg,
                "data": d,
                "replying": reply,
                "id": obj.id,
            },
        )

        return obj

    async def pend_message(
        self,
        msg: Optional[str] = None,
        data: Optional[Payload] = None,
        replying: Optional[Message] = None,
    ) -> PendingMessage:
        return PendingMessage(
            self,
            msg,
            data=data,
            replying=replying,
        )


_PY_BUILTINS = {str, float, int, bool, dict}


class Server(MessageListener):
    """Class for handling a server."""

    __slots__ = (
        "_token",
        "_hide_token",
        "_login_func",
        "_minimum_version",
        "_operations",
        "_supported_operations",
        "_unsupported_operations",
        "_clients",
        "_server",
        "_start_called",
        "_all_connections",
        "_is_fancy",
        "_exceptions",
    )

    def __init__(
        self,
        token: Optional[str] = None,
        *,
        default_token_len: int = 25,
        default_token_choices: "SupportsLenAndGetItem[str]" = ascii_letters,
        hide_token: bool = False,
        login_func: LoginFunc = _base_login,
        log_level: Optional[int] = None,
        minimum_version: Optional[VersionLike] = None,
        extra_operations: Optional[Operations] = None,
        unsupported_operations: Optional[Sequence[str]] = None,
        supported_operations: Optional[Sequence[str]] = None,
        extra_listeners: Optional[MessageListeners] = None,
        fancy: Optional[bool] = None,
    ) -> None:
        self._token: str = token or "".join(
            [choice(default_token_choices) for _ in range(default_token_len)],
        )
        self._hide_token = hide_token
        self._login_func = login_func

        if log_level:
            logging.getLogger("hoist").setLevel(log_level)

        self._minimum_version = minimum_version
        self._operations = {**BASE_OPERATIONS, **(extra_operations or {})}
        self._supported_operations = supported_operations or ["*"]
        self._unsupported_operations = unsupported_operations or []
        self._clients: List[Socket] = []
        self._server: Optional[UvicornServer] = None
        self._start_called: bool = False
        self._all_connections: List[Socket] = []
        self._is_fancy: Optional[bool] = fancy
        self._exceptions: List[Exception] = []
        super().__init__(extra_listeners)

    async def _call_operation(
        self,
        op: OperationData,
        payload: Payload,
    ) -> JSONLike:
        """Call an operation."""
        func = op[0]
        typ = op[1]
        custom_payload = op[2]

        if typ is OperatorParam.NONE:
            result = await func()  # type: ignore
        elif typ is OperatorParam.SERVER_ONLY:
            result = await func(self)  # type: ignore
        elif typ in {
            OperatorParam.PAYLOAD_ONLY,
            OperatorParam.SERVER_AND_PAYLOAD,
        }:
            if custom_payload:
                hints = get_type_hints(func)
                cl: Type = hints[tuple(hints.keys())[0]]

                verify_schema(get_type_hints(cl), payload)
                data = cl(**payload)
            else:
                data = payload  # type: ignore
            args = (
                (
                    self,
                    data,
                )
                if typ is OperatorParam.SERVER_AND_PAYLOAD
                else (data,)
            )
            result = await func(*args)  # type: ignore
        else:
            hints = get_type_hints(func)
            verify_schema(hints, payload)
            result = await func(**payload)  # type: ignore

        result_type = type(result)

        if (result_type in _PY_BUILTINS) or (not result):
            return result

        dct: Optional[dict] = getattr(result, "__dict__", None)

        if not dct:
            raise TypeError(
                f"operation handler {func.__name__} returned non-json type: {result_type}",  # noqa
            )

        return dct

    @property
    def fancy(self) -> bool:
        """Whether the server is running with fancy output."""
        return self._is_fancy or False

    @property
    def supported_operations(self) -> Sequence[str]:
        """Operations supported by the server."""
        return self._supported_operations

    @property
    def unsupported_operations(self) -> Sequence[str]:
        """Operations blacklisted by the server."""
        return self._unsupported_operations

    def _verify_operations(self) -> None:
        """Verify current operations lists."""
        so = self.supported_operations
        uo = self.unsupported_operations

        for i in {so, uo}:
            if "*" in i:
                if len(i) > 1:
                    raise ValueError(
                        '"*" should be the only operation',
                    )
                return

        for i in so:
            if i in uo:
                raise ValueError(
                    f'operation "{i}" is both supported and unsupported',
                )

    async def _verify_operation(  # not sure if i need async here
        self, operation: str
    ) -> bool:
        """Verify that an operation is supported by the server."""
        so = self.supported_operations
        uo = self.unsupported_operations

        if ("*" in uo) and (operation not in so):
            return False

        if operation in uo:
            return False

        if "*" in so:
            return not (operation in uo)

        return not (operation not in self.supported_operations)

    @property
    def token(self) -> str:
        """Authentication token used to connect."""
        return self._token

    @staticmethod
    async def _handle_schema(
        ws: Socket,
        payload: Payload,
        schema: Schema,
    ) -> List[Any]:
        """Verify a JSON object received from the user via a schema."""
        try:
            verify_schema(
                schema,
                payload,
            )
        except SchemaValidationError as e:
            await ws.error(
                INVALID_CONTENT,
                payload=invalid_payload(e),
            )

        return [payload[i] for i in schema]

    async def _process_operation(
        self,
        ws: Socket,
        payload: Payload,
        id: int,
    ) -> None:
        """Execute an operation."""
        operation, data = await self._handle_schema(
            ws,
            payload,
            {
                "operation": str,
                "data": dict,
            },
        )

        op = self._operations.get(operation)

        if not op:
            await ws.error(UNKNOWN_OPERATION)

        if not (await self._verify_operation(operation)):
            await ws.error(UNSUPPORTED_OPERATION)

        try:
            result = await self._call_operation(op, data)
        except SchemaValidationError as e:
            await ws.error(INVALID_CONTENT, payload=invalid_payload(e))

        await ws.success(id, payload={"result": result})

    async def _process_message(
        self,
        ws: Socket,
        payload: Payload,
        id: int,
    ) -> None:
        """Call message listeners."""
        message, data, replying = await self._handle_schema(
            ws,
            payload,
            {
                "message": str,
                "data": dict,
                "replying": (dict, None),
            },
        )

        transport = _SocketMessageTransport(ws, self, id)
        obj = await self.new_message(transport, message, data, replying)
        mid = obj.id

        await ws.success(
            id,
            payload={"id": mid},
            message=LISTENER_OPEN,
        )

        try:
            await self._call_listeners(
                transport,
                message,
                data,
                replying,
                mid,
            )
        except Exception as e:
            if isinstance(e, SchemaValidationError):
                await ws.error(INVALID_CONTENT, payload=invalid_payload(e))

            await self._internal_error(ws, e)

        await ws.success(id, message=LISTENER_CLOSE)

    async def _ws_wrapper(self, ws: Socket) -> None:
        """Main implementation of WebSocket logic."""
        version, token, id = await ws.recv(
            {
                "version": str,
                "token": str,
                "id": int,
            }
        )

        minver = self._minimum_version

        if minver:
            minver_actual = (
                minver
                if isinstance(minver, Version)
                else parse_version(minver)  # fmt: off
            )

            if not (parse_version(version) >= minver_actual):
                await ws.error(
                    BAD_VERSION,
                    payload={"needed": minver_actual.to_string()},
                )

        if not (await self._login_func(self, token)):
            await ws.error(LOGIN_FAILED)

        await ws.success(id)

        log(
            "login",
            f"{make_client(ws.address)} has successfully authenticated",  # noqa
        )

        while True:
            data: Payload
            action, data, nid = await ws.recv(
                {
                    "action": str,
                    "data": dict,
                    "id": int,
                }
            )

            if action == "operation":
                await self._process_operation(ws, data, nid)
            elif action == "message":
                await self._process_message(ws, data, nid)
            else:
                await ws.error(INVALID_ACTION)

    async def _ws(self, ws: Socket) -> None:
        """WebSocket entry point for Starlette."""  # noqa
        self._clients.append(ws)
        self._all_connections.append(ws)
        ws.status = Status.CONNECTED

        try:
            await self._ws_wrapper(ws)
        except Exception as e:
            ws.status = Status.KILLED
            log(
                "exc",
                f"{e.__class__.__name__}: {str(e) or '<no message>'}",
                level=logging.DEBUG,
            )
            addr = ws.address
            if isinstance(e, WebSocketDisconnect):
                log(
                    "disconnect",
                    f"unexpected disconnect{make_client_msg(addr)}",
                    level=logging.WARNING,
                )
            elif isinstance(e, ClientError):
                log(
                    "error",
                    f"connection from {make_client(addr)} encountered error {e.code} ([bold red]{e.error}[/]): [bold white]{e.message}",  # noqa
                    level=logging.ERROR,
                )
                await ws.close(1003)
            elif isinstance(e, CloseSocket):
                ws.status = Status.CLOSED
                await ws.close(1000)
            else:
                log(
                    "exception",
                    f"exception occured while receiving{make_client_msg(addr)}",  # noqa
                    level=logging.CRITICAL,
                )

                await self._internal_error(ws, e)
                await ws.close(1003)

        self._clients.remove(ws)

    async def _internal_error(
        self,
        ws: Socket,
        e: Exception,
    ):
        self._exceptions.append(e)

        if not self.fancy:
            print_exc(show_locals=True)

        with suppress(ClientError):
            await ws.error(
                SERVER_ERROR,
                payload={"message": str(e), "exc": e.__class__.__name__},
            )

    async def _app(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        """Main Starlette app implementation."""
        typ: str = scope["type"]

        if typ != "lifespan":
            path: str = scope["path"]
            hlog(
                "request" if typ == "http" else "websocket",
                f"[bold white]{path}[/] {scope}",
                level=logging.DEBUG,
            )

            if typ == "http":
                response: Response
                if path == "/hoist/ack":
                    msg = {"version": __version__}
                    hlog("ack", msg, level=logging.DEBUG)
                    response = JSONResponse(msg)
                else:
                    response = HTMLResponse(
                        HTML,
                    )
                await response(scope, receive, send)

            if typ == "websocket":
                if path == "/hoist":
                    socket = WebSocket(scope, receive, send)
                    obj = Socket(socket)
                    await obj.connect()

                    return await self._ws(obj)

                response = Response(
                    "Not found.",
                    media_type="text/plain",
                    status_code=404,
                )
                await response(scope, receive, send)

    @staticmethod
    def _ensure_none(url: URL):
        """Ensure that the target URL is not already being used."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((url.host, url.port))

        if not result:
            raise AlreadyInUseError(
                f"{url} is an existing server (did you forget to close it?)",  # noqa
            )

    def _fancy(self):
        with Live(screen=True) as live:
            while self.running:
                table = Table(
                    box=box.ROUNDED,
                    title=f"[bold cyan]Hoist {__version__}",
                )
                table.add_column("Address")
                table.add_column("Status")
                excs = self._exceptions
                rendered_table = Padding(Align.center(table), 1)

                layout = Layout(
                    rendered_table if not excs else None,
                )

                if excs:
                    lay = Layout()
                    lay.split_row(
                        *[
                            Panel(
                                "".join(
                                    format_exception(
                                        type(e),
                                        e,
                                        e.__traceback__,
                                    )
                                ),
                                title=f"[bold red]{e.__class__.__name__}",
                            )
                            for e in excs
                        ]
                    )

                    layout.split_column(
                        Layout(rendered_table, ratio=2),
                        lay,
                    )

                for i in self._all_connections:
                    table.add_row(
                        f"[bold cyan]{i.make_address()}",
                        i.rich_status,
                    )

                live.update(layout)

    def start(  # type: ignore
        self,
        *,
        host: str = "0.0.0.0",
        port: int = 5000,
        fancy: Optional[bool] = None,
    ) -> None:
        """Start the server."""
        if self.running:
            raise AlreadyInUseError(
                "server is already running (did you forget to call close?)",
            )

        self._is_fancy = fancy if fancy is not None else self._is_fancy
        fancy = self._is_fancy

        async def _app(
            scope: Scope,
            receive: Receive,
            send: Send,
        ) -> None:
            await self._app(scope, receive, send)

        self._ensure_none(
            URL.build(
                host=host,
                port=port,
                scheme="http",
            )
        )

        config = uvicorn.Config(_app, host=host, port=port, lifespan="on")
        self._server = UvicornServer(config)

        if fancy:
            logging.getLogger("hoist").setLevel(logging.ERROR)

        args = (
            self._hide_token,
            self.token,
        )

        try:
            if not fancy:
                self._server.run_in_thread(*args)
            else:
                with _CONSOLE.status("Starting...", spinner="bouncingBar"):
                    self._server.run_in_thread(*args)

                Thread(target=self._fancy).start()
        except RuntimeError as e:
            raise RuntimeError(
                "server cannot start from a running event loop",
            ) from e

        self._start_called = True

    async def broadcast(
        self,
        message: str,
        payload: Optional[Payload] = None,
    ) -> None:
        """Send a message to all connections."""
        if not self._server:
            raise ServerNotStartedError(
                "server is not started (did you forget to call start?)"
            )

        if not self._clients:
            log(
                "broadcast",
                "no clients are connected",
                level=logging.WARNING,
            )

        for i in self._clients:
            transport = _SocketMessageTransport(
                i,
                self,
                None,
                SINGLE_NEW_MESSAGE,
            )
            try:
                await transport.message(message, payload)
            except Exception as e:
                hlog(
                    "broadcast",
                    f"exception occured while sending: {type(e).__name__} - {e}",  # noqa
                    level=logging.WARNING,
                )

    def close(self) -> None:
        """Close the server."""
        if not self._server:
            hlp = (
                "call close twice"
                if self._start_called
                else "forget to call start"  # fmt: off
            )
            raise ServerNotStartedError(
                f"server is not started (did you {hlp}?)",
            )
        self._server.close_thread()
        self._server = None
        self._start_called = False

    @property
    def running(self) -> bool:
        """Whether the server is running."""
        return bool(self._server)

    def stop(self) -> None:
        """Alias to `Server.close`."""
        self.close()

    def operation(self, name: str):
        """Add a function for an operation."""

        def decorator(func: Operator):
            pl_type: bool = False
            op_type = OperatorParam.NONE
            params = inspect.signature(func).parameters

            if params:
                annotations = [i.annotation for i in params.values()]
                plen: int = len(params)
                first = annotations[0]

                if annotations == [Server]:
                    op_type = OperatorParam.SERVER_ONLY
                elif first == Server:
                    op_type = OperatorParam.SERVER_AND_PAYLOAD
                else:
                    if (first in _PY_BUILTINS) and (first is not dict):
                        op_type = OperatorParam.DYNAMIC
                    else:
                        op_type = (
                            OperatorParam.SERVER_AND_PAYLOAD
                            if plen == 2
                            else OperatorParam.PAYLOAD_ONLY
                            if plen == 1
                            else OperatorParam.DYNAMIC
                        )
            else:
                op_type = OperatorParam.NONE

            self._operations[name] = (
                func,
                op_type,
                pl_type,
            )

        return decorator
