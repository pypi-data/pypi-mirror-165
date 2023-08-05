import asyncio
import logging
import time
from threading import Thread
from typing import Optional

import uvicorn

from ._logging import hlog, log

__all__ = ("UvicornServer",)

# see https://github.com/encode/uvicorn/discussions/1103


class UvicornServer(uvicorn.Server):
    """Threadable uvicorn server."""

    __slots__ = ("_thread",)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._thread: Optional[Thread] = None

    def run_in_thread(
        self,
        hide_token: bool,
        token: str,
    ) -> None:
        """Run the server in a thread."""
        hlog(
            "startup",
            f"using event loop {asyncio.get_event_loop()}",
            level=logging.DEBUG,
        )
        thread = Thread(target=self.run)
        self._thread = thread
        thread.start()
        log("startup", "waiting for start...", level=logging.DEBUG)

        while not self.started:
            time.sleep(1e-3)

        tokmsg: str = (
            f" with token [bold blue]{token}[/]" if not hide_token else ""
        )  # fmt: off
        log(
            "startup",
            f"started server on [bold cyan]{self.config.host}:{self.config.port}[/]{tokmsg}",  # noqa
        )

    def close_thread(self):
        """Close the running thread."""
        self.should_exit = True
        t = self._thread
        log(
            "close",
            "joining thread...",
            level=logging.DEBUG,
        )

        if t:
            t.join()

        log(
            "shutdown",
            "server closed",
        )

        self._thread = None
