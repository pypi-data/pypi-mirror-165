import asyncio
import logging
from typing import (
    TYPE_CHECKING, Dict, Iterator, NamedTuple, Optional, TypeVar, overload
)

from aiohttp import ClientWebSocketResponse
from typing_extensions import Literal

from .__about__ import __version__
from ._errors import INVALID_CONTENT, SERVER_ERROR
from ._logging import hlog, log
from ._messages import (
    LISTENER_CLOSE, LISTENER_OPEN, NEW_MESSAGE, SINGLE_NEW_MESSAGE
)
from ._typing import Payload, TransportMessageListener
from ._warnings import warn
from .exceptions import (
    BadContentError, InternalServerError, InvalidVersionError,
    ServerLoginError, ServerResponseError
)

if TYPE_CHECKING:
    from .client import Connection

__all__ = ("ServerSocket",)


class _Response(NamedTuple):
    success: bool
    data: Optional[Payload]
    error: Optional[str]
    message: Optional[str]
    desc: Optional[str]
    code: int
    id: Optional[int]


T = TypeVar("T")


def _drain(queue: "asyncio.Queue[T]") -> Iterator[T]:
    """Drain the target queue."""
    while True:
        try:
            yield queue.get_nowait()
        except asyncio.QueueEmpty:
            break


"""
NOTE: can't generic asyncio.Queue directly due to compatibility with other versions
"""  # noqa


class ServerSocket:
    """Class for handling a WebSocket connection to a server."""

    __slots__ = (
        "_ws",
        "_token",
        "_logged",
        "_closed",
        "_message_listener",
        "_client",
        "_receiving",
        "_messages",
    )

    def __init__(
        self,
        client: "Connection",
        ws: ClientWebSocketResponse,
        token: str,
    ) -> None:
        self._ws = ws
        self._token = token
        self._logged: bool = False
        self._closed: bool = False
        self._message_listener: Optional[TransportMessageListener] = None
        self._client = client
        self._receiving: Dict[int, "asyncio.Queue[_Response]"] = {}
        self._messages: "asyncio.Queue[Payload]" = asyncio.Queue()

    @property
    def messages(self) -> asyncio.Queue:
        """Queue containing unprocessed messages."""
        return self._messages

    async def _rc(self) -> _Response:
        """Receive and parse a server response."""
        json = await self._ws.receive_json()
        hlog(
            "receive",
            json,
            level=logging.DEBUG,
        )
        return _Response(**json)

    async def _throw_error(self, res: _Response) -> None:
        error = res.error
        data = res.data
        message = res.message
        code = res.code
        assert error
        assert message

        if code == INVALID_CONTENT:
            assert data
            needed_raw = data["needed"]
            needed = (
                ", ".join(needed_raw)
                if isinstance(needed_raw, list)
                else needed_raw  # fmt: off
            )

            raise BadContentError(
                f'sent type {data["current"]} when server expected {needed}',  # noqa
            )

        elif code == SERVER_ERROR:
            assert data
            raise InternalServerError(
                f"exception occured on server: {data['exc']} - {data['message']}"  # noqa
            )

        raise ServerResponseError(
            f"code {code} [{error}]: {message}",
            code=res.code,
            error=error,
            message=message,
            payload=data,
        )

    async def _recv(self, id: int) -> _Response:
        """High level function to properly accept data from the server."""
        self._receiving[id] = asyncio.Queue(1)
        messages = self._messages
        res = await self._rc()

        data = res.data

        if res.code != 0:
            await self._throw_error(res)

        if res.message == SINGLE_NEW_MESSAGE:
            assert data
            messages.put_nowait(data)
            res = await self._recv(id)

        if res.message == LISTENER_OPEN:
            log(
                "listener",
                "now receiving",
                level=logging.DEBUG,
            )

            while True:
                new_res_json = await self._ws.receive_json()
                new_res = _Response(**new_res_json)

                hlog(
                    "listener receive",
                    new_res_json,
                    level=logging.DEBUG,
                )

                if new_res.code != 0:
                    await self._throw_error(new_res)

                if new_res.message == LISTENER_CLOSE:
                    break

                elif new_res.message in {NEW_MESSAGE, SINGLE_NEW_MESSAGE}:
                    data = new_res.data
                    assert data
                    messages.put_nowait(data)

            log(
                "listener",
                "done receiving",
                level=logging.DEBUG,
            )

        gqueue = self._receiving.get(id)

        assert res.id is not None, "response has no id"
        pqueue = self._receiving.get(res.id)

        if not gqueue:
            raise RuntimeError(
                f"(internal error) no receiver found for {res}",
            )

        if not pqueue:
            raise RuntimeError(
                f"{res} not in receivers",
            )

        pqueue.put_nowait(res)
        return await gqueue.get()

    async def process_messages(self):
        """Run message listeners with received messages."""
        listener = self._message_listener
        assert listener

        for i in _drain(self._messages):
            client = self._client

            await listener(
                client,
                i["message"],
                i["data"],
                i["replying"],
                i["id"],
            )

    async def login(self, listener: TransportMessageListener) -> None:
        """Send login message to the server."""
        self._message_listener = listener

        try:
            await self.send(
                {
                    "token": self._token,
                    "version": __version__,
                },
                0,
                reply=True,
            )
        except ServerResponseError as e:
            if e.code == 4:
                assert e.payload
                raise InvalidVersionError(
                    f"server needs version {e.payload['needed']}, but you have {__version__}",  # noqa
                )
            if e.code == 3:
                raise ServerLoginError("login token is not valid") from e

            raise e  # we shouldnt ever get here

        self._logged = True

    @property
    def logged(self) -> bool:
        """Whether the socket has authenticated with the server."""
        return self._logged

    async def close(self) -> None:
        """Close the socket."""
        log("close", "closing socket", level=logging.DEBUG)

        if not self._closed:
            await self.send({"end": True})
        else:
            warn("attempted to double close connection")

        self._closed = True

    @overload
    async def send(  # type: ignore
        self,
        payload: Payload,
        id: Optional[int] = None,
        *,
        reply: Literal[False] = False,
    ) -> Literal[None]:
        """Send a message to the server."""
        ...

    @overload
    async def send(
        self,
        payload: Payload,
        id: Optional[int] = None,
        *,
        reply: Literal[True] = True,
    ) -> _Response:
        """Send a message to the server."""
        ...

    async def send(
        self,
        payload: Payload,
        id: Optional[int] = None,
        *,
        reply: bool = False,
    ) -> Optional[_Response]:
        """Send a message to the server."""
        data = {"id": id, **payload}
        await self._ws.send_json(data)
        hlog("send", data, level=logging.DEBUG)

        if reply:
            assert id is not None, "id must be passed to receive"
            return await self._recv(id)

        return None
