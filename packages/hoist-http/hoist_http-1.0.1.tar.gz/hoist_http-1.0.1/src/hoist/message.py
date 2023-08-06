from abc import ABC, abstractmethod
from typing import Optional

from ._messages import BaseMessagable, MessageListener
from ._typing import Payload
from ._warnings import warn

__all__ = (
    "Message",
    "PendingMessage",
    "BaseMessage",
)


class BaseMessage(MessageListener, ABC):
    """Base class for handling a message."""

    __slots__ = (
        "_conn",
        "_msg",
        "_data",
        "_replying",
    )

    def __init__(
        self,
        conn: BaseMessagable,
        msg: str,
        *,
        data: Optional[Payload] = None,
        replying: Optional["Message"] = None,
    ) -> None:
        """Construct for `BaseMessage`.

        Args:
            conn: Messagable connection target.
            msg: Content of the message.
            data: Payload included with the message.
            replying: Message object that the current one is replying to.

        """
        self._conn = conn
        self._msg = msg
        self._data = data or {}
        self._replying = replying
        super().__init__()

    @property
    def content(self) -> str:
        """Message content."""
        return self._msg

    @property
    def data(self) -> Payload:
        """Raw message payload."""
        return self._data

    @property
    def replying(self) -> Optional["Message"]:
        """Message that the current message is replying to."""
        return self._replying

    @abstractmethod
    def to_dict(
        self,
        convert_replies: bool = True,
    ) -> dict:
        """Convert the message to a dictionary.

        Args:
            convert_replies: Should message objects under `replying` be converted to a `dict`.

        Returns:
            The created `dict` object.
        """  # noqa
        ...

    def __repr__(self) -> str:
        values = [
            f"{k}={repr(v)}"
            for k, v in self.to_dict(
                convert_replies=False,
            ).items()
        ]
        return f"{self.__class__.__name__}({', '.join(values)})"


class Message(BaseMessage):
    """Object handling a message."""

    __slots__ = ("_id",)

    def __init__(
        self,
        conn: BaseMessagable,
        msg: str,
        id: int,
        *,
        data: Optional[Payload] = None,
        replying: Optional["Message"] = None,
    ) -> None:
        self._id = id
        super().__init__(conn, msg, data=data, replying=replying)

    @property
    def id(self) -> int:
        """Message ID."""
        return self._id

    async def reply(
        self,
        msg: str,
        data: Optional[Payload] = None,
    ) -> "Message":
        """Reply to the current message.

        Args:
            msg: Content to reply with.
            data: Payload to include in the reply.

        Returns:
            Created message.
        """
        return await self._conn.message(msg, data or {}, replying=self)

    def to_dict(  # noqa
        self,
        convert_replies: bool = True,
    ) -> dict:
        reply = self.replying

        return {
            "replying": (reply.to_dict() if reply else None)
            if convert_replies
            else reply,
            "id": self.id,
            "data": self.data,
            "message": self.content,
        }

    def receive(self, *args, **kwargs):  # noqa
        warn(
            "receive() should not be called on a message object\nif you would like to handle replies, please use message_later()",  # noqa
        )
        return super().receive(*args, **kwargs)


class PendingMessage(BaseMessage):
    """Object handling a message that has not yet been sent to the server."""

    def __init__(
        self,
        conn: BaseMessagable,
        msg: Optional[str] = None,
        *,
        data: Optional[Payload] = None,
        replying: Optional["Message"] = None,
    ) -> None:
        super().__init__(conn, msg or "", data=data, replying=replying)

    @property
    def content(self) -> str:  # noqa
        return self._msg

    @content.setter
    def content(self, value: str) -> None:
        self._msg = value

    def to_dict(  # noqa
        self,
        convert_replies: bool = True,
    ) -> dict:
        reply = self.replying

        return {
            "replying": (reply.to_dict() if reply else None)
            if convert_replies
            else reply,
            "data": self.data,
            "message": self.content,
        }

    async def send(self) -> Message:
        """Send the message.

        Returns:
            Created message.
        """
        return await self._conn.message(
            self.content,
            self.data,
            self.replying,
            listeners=self.message_listeners,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.send()
