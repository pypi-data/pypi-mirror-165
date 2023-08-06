import inspect
import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import (
    TYPE_CHECKING, Any, AsyncIterator, Dict, List, NamedTuple, Optional, Tuple,
    TypeVar, Union, get_type_hints
)

from typing_extensions import Final

from ._logging import hlog, log
from ._schema import verify_schema
from ._typing import DataclassLike, Listener, MessageListeners, Payload, Schema
from ._warnings import warn
from .exceptions import SchemaValidationError

if TYPE_CHECKING:
    from .message import Message, PendingMessage

from contextlib import asynccontextmanager, suppress

__all__ = (
    "MessageListener",
    "BaseMessagable",
    "ListenerParam",
)

T = TypeVar("T", bound=DataclassLike)

NEW_MESSAGE: Final[str] = "newmsg"
LISTENER_OPEN: Final[str] = "open"
LISTENER_CLOSE: Final[str] = "done"
SINGLE_NEW_MESSAGE: Final[str] = "s_newmsg"


class ListenerParam(Enum):
    """Type of parameter(s) that the listener should take."""

    NONE = 1
    MESSAGE_ONLY = 2
    MESSAGE_AND_PAYLOAD = 3


class ListenerData(NamedTuple):

    listener: Listener
    param: Optional[Union[DataclassLike, Schema]]
    param_type: ListenerParam


async def _process_listeners(
    listeners: Optional[List[ListenerData]],
    message: "Message",
    *,
    hide_warning: bool = False,
) -> None:
    hlog(
        "listeners",
        f"processing list - {listeners}",
        level=logging.DEBUG,
    )

    called = False
    schema_failed: List[str] = []

    for i in listeners or ():
        # TODO: clean up type safety here
        func = i.listener
        param = i.param
        typ = i.param_type
        called = True

        if typ is ListenerParam.NONE:
            await func()  # type: ignore
            continue

        if typ is ListenerParam.MESSAGE_ONLY:
            await func(message)  # type: ignore
            continue

        is_schema: bool = isinstance(param, dict)
        schema: Any = param if is_schema else get_type_hints(param)

        try:
            verify_schema(schema, message.data)
        except SchemaValidationError:
            schema_failed.append(func.__name__)
            called = False
            continue

        payload = message.data
        await func(
            message,  # type: ignore
            payload if is_schema else param(**payload),  # type: ignore
        )

    if (not called) and ((not hide_warning) or listeners):
        failed: str = (
            f' (function{"s" if len(schema_failed) > 1 else ""} [bold green]{"[/], [bold green]".join(schema_failed)}[/] failed schema validation, enable debug logging for more info)'  # noqa
            if schema_failed
            else ""
        )
        warn(
            f'received "{message.content}", but no listeners were called{failed}',  # noqa
        )


class MessageListener:
    """Base class for handling message listening."""

    __slots__ = (
        "_message_listeners",
        "_current_id",
        "_all_messages",
    )

    def __init__(
        self,
        extra_listeners: Optional[MessageListeners] = None,
    ):
        self._message_listeners: MessageListeners = {
            **(extra_listeners or {}),
        }
        self._current_id = 0
        self._all_messages: Dict[int, "Message"] = {}

    @property
    def message_listeners(self) -> MessageListeners:
        """Listener function for messages."""
        return self._message_listeners

    @message_listeners.setter
    def message_listeners(self, value: MessageListeners) -> None:
        self._message_listeners = value

    async def _call_listeners(
        self,
        ws: "BaseMessagable",
        message: str,
        payload: Payload,
        replying: Optional[dict],
        id: int,
    ) -> None:
        ml = self.message_listeners
        listeners = ml.get(message)
        obj = await self.create_or_lookup(
            ws,
            message,
            payload,
            id,
            replying,
        )
        reply = obj.replying

        if reply:
            await _process_listeners(
                reply.message_listeners.get(message),
                reply,
                hide_warning=True,
            )

        await _process_listeners(listeners, obj)

        glbl = ml.get(None)
        await _process_listeners(
            glbl,
            obj,
            hide_warning=True,
        )

    def receive(
        self,
        message: Optional[Union[str, Tuple[str, ...]]] = None,
        parameter: Optional[Union[Schema, T]] = None,
    ):
        """Add a listener for message receiving.

        Args:
            message: Message to listen for.
            parameter: Parameter type to use.
        """

        def decorator(func: Listener):
            listeners = self.message_listeners

            param: Optional[Union[DataclassLike, Schema]] = parameter

            if not param:
                hints = get_type_hints(func)
                if hints:
                    with suppress(IndexError):
                        param = hints[tuple(hints.keys())[1]]

            params = len(inspect.signature(func).parameters)
            value = ListenerData(
                func,
                param or dict,
                ListenerParam.NONE
                if not params
                else ListenerParam.MESSAGE_ONLY
                if params == 1
                else ListenerParam.MESSAGE_AND_PAYLOAD,
            )

            if message in listeners:
                listeners[message].append(value)  # type: ignore
            else:
                if not isinstance(message, tuple):
                    listeners[message] = [value]
                else:
                    for i in message:
                        if i in listeners:
                            listeners[i].append(value)
                        else:
                            listeners[i] = [value]

        return decorator

    @property
    def current_id(self) -> int:
        """Current message ID."""
        return self._current_id

    async def create_message(
        self,
        conn: "BaseMessagable",
        data: Payload,
    ) -> "Message":
        """Build a message from a payload.

        Args:
            conn: Messagable connection target.
            data: Payload to create the message from.
        """
        mid: int = data["id"]
        self._all_messages[mid] = await self._build_message(conn, data)
        return self._all_messages[mid]

    async def create_or_lookup(
        self,
        conn: "BaseMessagable",
        content: str,
        message_data: Payload,
        id: int,
        replying: Optional[Union["Message", dict]],
        *,
        listeners: Optional[MessageListeners] = None,
    ) -> "Message":
        """Create a new message wtih the specified ID, or look it up if it already exists.

        Args:
            conn: Messagable connection target.
            content: Message content.
            message_data: Payload to include with the message.
            id: ID of the message:
            replying: Message that the target is replying to.
            listeners: Extra message listeners.

        Returns:
            Created message.
        """  # noqa
        mid: int = id
        obj = self._all_messages.get(mid)

        if obj:
            hlog(
                "create or lookup",
                f"using existing {obj}",
                level=logging.DEBUG,
            )
            return obj

        log(
            "create or lookup",
            f"id {mid} does not exist, creating it",
            level=logging.DEBUG,
        )
        obj = await self.new_message(
            conn,
            content,
            message_data,
            replying,
            id=id,
            listeners=listeners,
        )

        if listeners:
            obj.message_listeners = listeners

        return obj

    async def new_message(
        self,
        conn: "BaseMessagable",
        content: str,
        message_data: Payload,
        replying: Optional[Union["Message", dict]],
        *,
        id: Optional[int] = None,
        listeners: Optional[MessageListeners] = None,
    ) -> "Message":
        """Create a new message.

        Args:
            conn: Messagable connection target.
            content: Message content.
            message_data: Payload to include with the message.
            id: ID of the message:
            replying: Message that the target is replying to.
            listeners: Extra message listeners.

        Returns:
            Created message.

        Raises:
            ValueError: Message ID is already in use.
        """
        from .message import Message

        self._current_id += 1
        mid = id or self._current_id

        if mid in self._all_messages:
            raise ValueError(
                f"message {id} has already been created",
            )

        obj = Message(
            conn,
            content,
            mid,
            data=message_data,
            replying=replying
            if not isinstance(replying, dict)
            else await self._build_message(
                conn,
                replying,
            ),
        )

        if listeners:
            obj.message_listeners = listeners

        self._all_messages[mid] = obj
        hlog(
            "message create",
            f"constructed new message {obj}",
            level=logging.DEBUG,
        )
        return obj

    async def lookup(self, id: int) -> "Message":
        """Lookup a message by its ID.

        Args:
            id: ID of the message to lookup.

        Raises:
            ValueError: Message ID does not exist.
        """
        try:
            obj = self._all_messages[id]
        except KeyError as e:
            raise ValueError(
                f"(internal error) message {id} does not exist",
            ) from e
        hlog(
            "message lookup",
            f"looked up {obj}",
            level=logging.DEBUG,
        )
        return obj

    async def _build_message(
        self,
        conn: "BaseMessagable",
        data: Payload,
    ) -> "Message":
        """Generate a message object from a payload."""
        return await self.create_or_lookup(
            conn,
            data["message"],
            data["data"],
            data["id"],
            data["replying"],
        )


class BaseMessagable(ABC):
    """Abstract class representing a messagable target."""

    async def pend_message(
        self,
        msg: Optional[str] = None,
        data: Optional[Payload] = None,
        replying: Optional["Message"] = None,
    ) -> "PendingMessage":
        """Get a message to be sent later.

        Args:
            msg: Message content.
            data: Payload to include with the message.
            replying: Message to reply to.
        """
        from .message import PendingMessage

        return PendingMessage(
            self,
            msg,
            data=data,
            replying=replying,
        )

    @asynccontextmanager
    async def message_later(
        self,
        msg: Optional[str] = None,
        data: Optional[Payload] = None,
        replying: Optional["Message"] = None,
    ) -> AsyncIterator["PendingMessage"]:
        """Send a message after the context has finished.

        Args:
            msg: Message content.
            data: Payload to include with the message.
            replying: Message to reply to.
        """
        from .message import PendingMessage

        obj = PendingMessage(
            self,
            msg,
            data=data,
            replying=replying,
        )
        try:
            yield obj
        finally:
            await obj.send()

    @abstractmethod
    async def message(
        self,
        msg: str,
        data: Optional[Payload] = None,
        replying: Optional["Message"] = None,
        listeners: Optional[MessageListeners] = None,
    ) -> "Message":
        """Send a message.

        Args:
            msg: Message content.
            data: Payload to include with the message.
            replying: Message to reply to.
            listeners: Extra listeners to include.

        Returns:
            Created message.
        """
        ...
