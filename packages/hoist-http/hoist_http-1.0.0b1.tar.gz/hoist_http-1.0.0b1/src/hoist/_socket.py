import json
import logging
from enum import Enum
from typing import Any, Dict, List, NoReturn, Optional

from starlette.datastructures import Address
from starlette.websockets import WebSocket

from ._errors import ERRORS, INVALID_CONTENT, INVALID_JSON
from ._logging import hlog, log
from ._schema import invalid_payload, verify_schema
from ._typing import Payload, Schema
from .exceptions import ClientError, CloseSocket, SchemaValidationError

__all__ = (
    "make_client_msg",
    "make_client",
    "Socket",
    "Status",
)


def make_client_msg(addr: Optional[Address], to: bool = False) -> str:
    """Create a client message."""
    target: str = "from" if not to else "to"
    return f" {target} [bold cyan]{addr.host}:{addr.port}[/]" if addr else ""


def make_client(addr: Optional[Address]) -> str:
    """Make a client string."""
    return f"[bold cyan]{addr.host}:{addr.port}[/]" if addr else "client"


class Status(Enum):
    """Current connection status."""

    AUTHENTICATING = 1
    CONNECTED = 2
    CLOSED = 3
    KILLED = 4


_RICH_STATUSES: Dict[Status, str] = {
    Status.AUTHENTICATING: "[bold yellow]Authenticating",
    Status.CONNECTED: "[bold green]Connected",
    Status.CLOSED: "[bold red]Closed",
    Status.KILLED: "[bold dim red]Killed",
}


class Socket:
    """Class for handling a WebSocket."""

    __slots__ = (
        "_ws",
        "_logged",
        "_status",
    )

    def __init__(
        self,
        ws: WebSocket,
    ):
        self._ws = ws
        self._logged: bool = False
        self._status: Status = Status.AUTHENTICATING

    def make_address(self) -> str:
        """Get the current address as rich text."""
        addr = self.address
        return "[bold yellow]?[/]" if not addr else f"{addr.host}:{addr.port}"

    @property
    def status(self) -> Status:
        """Current connection status."""
        return self._status

    @status.setter
    def status(self, value: Status) -> None:
        self._status = value

    @property
    def rich_status(self) -> str:
        """Rich connection status."""
        return _RICH_STATUSES[self.status]

    async def connect(self) -> None:
        """Establish the WebSocket connection."""
        ws = self._ws
        await ws.accept()

        log(
            "connect",
            f"connecting{make_client_msg(ws.client, to=True)}",
        )

    @property
    def ws(self) -> WebSocket:
        """Raw WebSocket object."""
        return self._ws

    @property
    def logged(self) -> bool:
        """The authentication status of the current connection."""
        return self._logged

    @logged.setter
    def logged(self, value: bool) -> None:
        self._logged = value

    async def _send(
        self,
        id: Optional[int],
        *,
        success: bool = True,
        payload: Optional[Payload] = None,
        code: int = 0,
        error: Optional[str] = None,
        message: Optional[str] = None,
        desc: Optional[str] = None,
    ) -> None:
        """Send a message to the client."""
        content = {
            "success": success,
            "data": payload,
            "error": error,
            "code": code,
            "message": message,
            "desc": desc,
            "id": id,
        }
        hlog("send", content, level=logging.DEBUG)
        await self.ws.send_json(content)

    async def error(
        self,
        code: int,
        *,
        id: Optional[int] = None,
        description: Optional[str] = None,
        payload: Optional[Payload] = None,
    ) -> NoReturn:
        """Send an error to the client."""
        err = ERRORS[code]
        error = err[0]
        message = err[1]

        await self._send(
            id,
            code=code,
            desc=description,
            error=error,
            message=message,
            payload=payload,
            success=False,
        )
        raise ClientError(code=code, error=error, message=message)

    async def success(
        self,
        id: Optional[int],
        payload: Optional[Payload] = None,
        *,
        message: Optional[str] = None,
    ) -> None:
        """Send a success to the client."""
        await self._send(
            id,
            code=0,
            message=message,
            payload=payload,
        )

    async def recv(self, schema: Schema) -> List[Any]:
        """Receive a set of keys from the client."""
        try:
            text = await self.ws.receive_text()
            load: Dict[Any, Any] = json.loads(text)
        except json.JSONDecodeError:
            await self.error(INVALID_JSON)

        hlog("receive", load, level=logging.DEBUG)

        if load.get("end"):
            raise CloseSocket

        try:
            verify_schema(schema, load)
        except SchemaValidationError as e:
            await self.error(INVALID_CONTENT, payload=invalid_payload(e))

        return [load[i] for i in schema]

    async def recv_only(self, schema: Schema) -> Any:
        """Receive a single key from the client."""
        return (await self.recv(schema))[0]

    async def close(self, code: int) -> None:
        """Gracefully close the connection."""
        log(
            "disconnect",
            f"no longer receiving{make_client_msg(self.ws.client)}",
        )
        await self.ws.close(code)

    @property
    def address(self) -> Optional[Address]:
        """Address object of the connection."""
        return self.ws.client
