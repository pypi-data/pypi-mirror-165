from enum import Enum
from typing import TypeVar

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
    return 1


BASE_OPERATIONS: Operations = {
    "print": (
        _print,
        OperatorParam.DYNAMIC,
        True,
    )
}
