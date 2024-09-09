"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from enconnect.irc import ClientEvent

from ...robie.models import RobieMessage

if TYPE_CHECKING:
    from ...robie import Robie
    from ...robie.childs import RobieClient
    from ...robie.models import RobieCommand
    from ...robie.models import RobieMessageKinds



@dataclass
class IRCMessage(RobieMessage):
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
    ) -> Literal['irc']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'irc'


    @property
    def kind(
        self,
    ) -> 'RobieMessageKinds':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.event.kind


    @property
    def isme(
        self,
    ) -> bool:
        """
        Return the boolean indicating message origin from client.

        :returns: Boolean indicating message origin from client.
        """

        return self.event.isme


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
        kind = event.kind


        target: Optional[str] = None

        if kind == 'chanmsg':
            target = event.recipient

        if kind == 'privmsg':
            target = event.author

        assert target is not None


        return client.compose(
            target, content)
