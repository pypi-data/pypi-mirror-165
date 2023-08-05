import asyncio
import inspect
import logging
import os
from contextlib import asynccontextmanager, contextmanager
from typing import Any, Awaitable, Callable, Coroutine, Optional, Union

from rich.console import Console

from ._typing import UrlLike
from .client import Connection
from .server import Server

__all__ = (
    "main",
    "connect",
    "start",
    "connect_with",
    "debug",
    "serve",
    "connect_directly",
)

print_exc = Console().print_exception


def main(func: Callable[[], Coroutine[Any, Any, Any]]) -> None:
    """Run a main async function.

    Args:
        func: Function to call.

    Example:
        ```py
        @hoist.main
        async def main() -> None:
            ...
        ```
    """
    frame = inspect.currentframe()
    assert frame
    assert frame.f_back

    if frame.f_back.f_globals["__name__"] == "__main__":
        try:
            asyncio.run(func())
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                return

            print_exc(show_locals=True)


@asynccontextmanager
async def connect(
    token: str,
    url: UrlLike = "http://localhost:5000",
    **kwargs: Any,
):
    """Connect to a Hoist server.

    Args:
        token: Token to use when connecting.
        url: Target server URL.

    Example:
        ```py
        async with hoist.connect("target token") as c:
            ...
        ```
    """
    try:
        conn = Connection(url, token, **kwargs)
        await conn.connect()
        yield conn
    finally:
        await conn.close()


async def connect_directly(
    token: str,
    url: UrlLike = "http://localhost:5000",
    **kwargs: Any,
):
    """Connect to a Hoist server without a context manager.

    Args:
        token: Token to use when connecting.
        url: Target server URL.

    Example:
        ```py
        server = await hoist.connect_directly("...")
        ```
    """
    conn = Connection(url, token, **kwargs)
    await conn.connect()
    return conn


@contextmanager
def serve(
    token: Optional[str] = None,
    server: Optional[Server] = None,
    *,
    host: str = "0.0.0.0",
    port: int = 5000,
    **kwargs,
):
    """Serve a Hoist server.

    Args:
        token: Token to use on the server.
        server: Existing server to use.
        host: Where to host the server.
        port: What port to put the server on.

    Example:
        ```py
        with hoist.serve("my authentication token") as server:
            ...
        ```
    """
    try:

        srvr = server or Server(token, **kwargs)
        srvr.start(host=host, port=port)
        yield srvr
    finally:
        srvr.close()


def connect_with(
    token: str,
    url: UrlLike = "http://localhost:5000",
    **kwargs: Any,
):
    """Call a function with the connection.

    Args:
        token: Token to use when connecting.
        url: Target server URL.

    Example:
        ```py
        @hoist.connect_with("...")
        async def conn(server: hoist.Connection):
            ...
        ```
    """

    def inner(func: Callable[[Connection], Awaitable[Any]]):
        async def _wrapper():
            conn = Connection(url, token, **kwargs)

            try:
                await conn.connect()
                await func(conn)
            except BaseException as e:
                if isinstance(e, KeyboardInterrupt):
                    return

                print_exc(show_locals=True)
            finally:
                if not conn.closed:
                    await conn.close()

        coro = _wrapper()

        try:
            asyncio.run(coro)
        except RuntimeError:
            asyncio.get_event_loop().create_task(coro)

    return inner


def start(
    token: Optional[str] = None,
    server: Optional[Server] = None,
    *,
    host: str = "0.0.0.0",
    port: int = 5000,
    fancy: bool = False,
    **kwargs,
) -> Server:
    """Start a Hoist server.

    Args:
        token: Token to use on the server.
        server: Existing server to use.
        host: Where to host the server.
        port: What port to put the server on.
        fancy: Whether fancy output should be enabled.

    Returns:
        Started server object.

    Example:
        ```py
        server = hoist.start("my token", host="localhost", port=5001)
        ```
    """
    srvr = server or Server(token, **kwargs)
    srvr.start(host=host, port=port, fancy=fancy)
    return srvr


def debug(
    *,
    trace: Union[bool, str] = False,
    enable_uvicorn: bool = False,
) -> None:
    """Enable debug logging.

    Args:
        trace: Should debug tracing should be enabled.
        enable_uvicorn: Should uvicorn logs be enabled.
    """
    logging.getLogger("hoist").setLevel(logging.DEBUG)
    os.environ["HOIST_TRACE"] = (
        trace if not isinstance(trace, bool) else "all" if trace else ""
    )

    if enable_uvicorn:
        logging.getLogger("uvicorn.error").disabled = False
        logging.getLogger("uvicorn.access").disabled = False
