"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Literal
from typing import TYPE_CHECKING

from enconnect.discord import ClientEvent

from ...robie.models import RobieMessage

if TYPE_CHECKING:
    from ...robie import Robie
    from ...robie.childs import RobieClient
    from ...robie.models import RobieCommand
    from ...robie.models import RobieMessageKinds



@dataclass
class DSCMessage(RobieMessage):
    """
    Contain information for sharing using the Python queue.
    """

    event: ClientEvent


    def __init__(
        self,
        client: 'RobieClient',
        event: ClientEvent,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.event = event

        super().__init__(client=client)


    @property
    def family(
        self,
    ) -> Literal['discord']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'discord'


    @property
    def kind(
        self,
    ) -> 'RobieMessageKinds':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.event.kind


    def reply(
        self,
        robie: 'Robie',
        content: str,
    ) -> 'RobieCommand':
        """
        Compose the message and transmit using the chat client.

        :param robie: Primary class instance for Chatting Robie.
        :param content: Content that will be source of message.
        """

        childs = robie.childs
        clients = childs.clients

        client = clients[
            self.client]

        event = self.event


        target = event.recipient

        assert target is not None


        return client.compose(
            target[1], content)


    def isme(
        self,
        robie: 'Robie',
    ) -> bool:
        """
        Return the boolean indicating message origin from client.

        .. note::
           Completely redundant with the other chatting clients.
           Currently the event attribute is not in parent class.

        :param robie: Primary class instance for Chatting Robie.
        :returns: Boolean indicating message origin from client.
        """

        from .client import DSCClient

        childs = robie.childs
        clients = childs.clients

        event = self.event

        _client = clients[
            self.client]

        assert isinstance(
            _client, DSCClient)

        client = _client.client

        if client is None:
            return False

        return event.isme(client)