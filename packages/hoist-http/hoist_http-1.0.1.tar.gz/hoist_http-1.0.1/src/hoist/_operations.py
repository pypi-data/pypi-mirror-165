from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar

import aiohttp

from ._typing import Operations

__all__ = ("BASE_OPERATIONS", "OperatorParam")


class OperatorParam(Enum):
    """Operator parameter type."""

    NONE = 1
    SERVER_ONLY = 2
    PAYLOAD_ONLY = 3
    SERVER_AND_PAYLOAD = 4
    DYNAMIC = 5


T = TypeVar("T")


async def _print(text: str):
    print(text)


async def _get(url: str):
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as s:
            return s.text


async def _read(path: str):
    return Path.read_text(Path(path))


def _make(
    fn: Callable[..., Any],
    *,
    name: Optional[str] = None,
):
    return {
        name
        or fn.__name__[1:]: (  # noqa
            fn,
            OperatorParam.DYNAMIC,
            True,
        )
    }


BASE_OPERATIONS: Operations = {
    **_make(_print),
    **_make(_get),
    **_make(_read),
}
