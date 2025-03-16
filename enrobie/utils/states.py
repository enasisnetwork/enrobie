"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Callable
from typing import Optional
from typing import TYPE_CHECKING

from encommon.types import BaseModel
from encommon.types import NCNone

from pydantic import Field

if TYPE_CHECKING:
    from ..robie.models import RobieMessage



class ClientChannel(BaseModel, extra='forbid'):
    """
    Cache the information regarding client status on server.
    """

    unique: Annotated[
        str,
        Field(...,
              description='Unique ID of channel on server',
              min_length=1)]

    title: Annotated[
        Optional[str],
        Field(None,
              description='Friendly human name of channel',
              min_length=1)]

    topic: Annotated[
        Optional[str],
        Field(None,
              description='Current topic for the channel',
              min_length=1)]

    members: Annotated[
        Optional[set[str]],
        Field(None,
              description='Current members of the channel',
              min_length=1)]


    def __init__(
        # NOCVR
        self,
        /,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(**data)



class ClientChannels:
    """
    Cache the information regarding client status on server.

    :param client: Client class instance for Chatting Robie.
    """

    __cached: dict[str, ClientChannel]


    def __init__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__cached = {}


    def create(
        self,
        unique: str,
    ) -> None:
        """
        Create the channel within the internal cache dictionary.

        :param unique: Unique identifier for channel on server.
        """

        cached = self.__cached

        item = ClientChannel(
            unique=unique)

        cached[unique] = item


    def select(
        self,
        unique: str,
    ) -> Optional[ClientChannel]:
        """
        Select the channel within the internal cache dictionary.

        :param unique: Unique identifier for channel on server.
        :returns: Channel within the internal cache dictionary.
        """

        cached = self.__cached

        names = {
            x.title: x.unique
            for x in
            cached.values()}

        if unique not in cached:

            if unique not in names:
                return None

            unique = names[unique]

        return cached[unique]


    def delete(
        self,
        unique: str,
    ) -> None:
        """
        Delete the channel within the internal cache dictionary.

        :param unique: Unique identifier for channel on server.
        """

        cached = self.__cached

        del cached[unique]


    def set_title(
        self,
        unique: str,
        title: str,
    ) -> None:
        """
        Update attribute for channel and create when not exists.

        :param unique: Unique identifier for channel on server.
        :param title: Proper huamn friendly name of the channel.
        """

        cached = self.__cached

        if unique not in cached:
            self.create(unique)

        select = self.select(unique)

        assert select is not None

        select.title = title or None


    def set_topic(
        self,
        unique: str,
        topic: str,
    ) -> None:
        """
        Update attribute for channel and create when not exists.

        :param unique: Unique identifier for channel on server.
        :param topic: Topic for discussion within the channel.
        """

        cached = self.__cached

        if unique not in cached:
            self.create(unique)

        select = self.select(unique)

        assert select is not None

        select.topic = topic or None


    def add_member(
        self,
        unique: str,
        member: str,
    ) -> None:
        """
        Update attribute for channel and create when not exists.

        :param unique: Unique identifier for channel on server.
        :param member: Remember relevant to the cache operation.
        """

        cached = self.__cached

        if unique not in cached:
            self.create(unique)

        select = self.select(unique)

        assert select is not None

        if not select.members:
            select.members = set()

        members = select.members

        members.add(member)


    def del_member(
        self,
        unique: str,
        member: str,
    ) -> None:
        """
        Update attribute for channel and create when not exists.

        :param unique: Unique identifier for channel on server.
        :param member: Remember relevant to the cache operation.
        """

        cached = self.__cached

        if unique not in cached:
            return NCNone

        select = self.select(unique)

        assert select is not None

        if not select.members:
            return NCNone

        members = select.members

        members.remove(member)

        if len(members) == 0:
            select.members = None


    def clear_members(
        self,
        unique: str,
    ) -> None:
        """
        Update attribute for channel and create when not exists.

        :param unique: Unique identifier for channel on server.
        """

        cached = self.__cached

        if unique not in cached:
            return NCNone

        select = self.select(unique)

        assert select is not None

        if not select.members:
            return NCNone

        select.members = None


    def rename_member(
        self,
        current: str,
        update: str,
    ) -> None:
        """
        Update attribute for channel and create when not exists.

        :param current: Current member name to be be searched.
        :param update: Value to replace current when is found.
        """

        cached = (
            self.__cached
            .values())

        for channel in cached:

            members = channel.members

            if members is None:
                continue

            if current not in members:
                continue

            members.remove(current)
            members.add(update)



class ClientPublish:
    """
    Allow for subscription to client events useful in tests.
    """

    __callbacks: list[Callable[['RobieMessage'], None]]


    def __init__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__callbacks = []


    def subscribe(
        self,
        callback: Callable[['RobieMessage'], None],
    ) -> None:
        """
        Store the callback within internal subscriber reference.

        :param callback: Function that will be called with item.
        """

        callbacks = self.__callbacks

        callbacks.append(callback)


    def publish(
        self,
        mitem: 'RobieMessage',
    ) -> None:
        """
        Submit the message from client to subscriber references.

        :param mitem: Item containing information for operation.
        """

        callbacks = self.__callbacks

        for callback in callbacks:
            callback(mitem)
