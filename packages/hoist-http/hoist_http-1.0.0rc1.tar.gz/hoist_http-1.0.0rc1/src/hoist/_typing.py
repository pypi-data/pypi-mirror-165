from typing import (
    TYPE_CHECKING, Any, Awaitable, Callable, Dict, List, Optional, Tuple, Type,
    Union
)

from typing_extensions import Protocol

if TYPE_CHECKING:
    from versions import Version
    from yarl import URL

    from ._messages import BaseMessagable, ListenerData
    from ._operations import OperatorParam
    from .message import Message
    from .server import Server


class DataclassLike(Protocol):
    """Dataclass-like object protocl."""

    __annotations__: Dict[str, Any]

    def __init__(self, *args, **kwargs) -> None:
        ...


_PyBuiltins = Union[str, float, int, bool, dict, None]
JSONLike = Union[_PyBuiltins, type]
Payload = Dict[str, Any]
Operator = Union[
    Callable[[Any], Awaitable[JSONLike]],
    Callable[[], Awaitable[JSONLike]],
    Callable[["Server", Any], Awaitable[JSONLike]],
    Callable[["Server"], Awaitable[JSONLike]],
]
_SchemaType = Optional[Type[Any]]
SchemaNeededType = Union[
    Type[Any],
    Union[Tuple[_SchemaType, ...], List[_SchemaType]],
]
Schema = Dict[str, SchemaNeededType]
OperationData = Tuple[Operator, "OperatorParam", bool]
Operations = Dict[str, OperationData]
UrlLike = Union[str, "URL"]
LoginFunc = Callable[["Server", str], Awaitable[bool]]
ResponseErrors = Dict[int, Tuple[str, str]]
Listener = Union[
    Callable[["Message", Any], Awaitable[None]],
    Callable[["Message"], Awaitable[None]],
    Callable[[], Awaitable[None]],
]
MessageListeners = Dict[
    Optional[str],
    List["ListenerData"],
]
VersionLike = Union[str, "Version"]


TransportMessageListener = Callable[
    ["BaseMessagable", str, Payload, Optional[dict], int],
    Awaitable[None],
]
