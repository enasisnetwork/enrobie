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

        robie = client.robie

        self.event = event

        person = (
            robie.person(
                client,
                event.author[1])
            if event.author
            else None)

        super().__init__(
            client=client,
            person=person)


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


    @property
    def isme(
        self,
    ) -> bool:
        """
        Return the boolean indicating message origin from client.

        :returns: Boolean indicating message origin from client.
        """

        return self.event.isme


    @property
    def hasme(
        self,
    ) -> bool:
        """
        Return the boolean indicating message mention the client.

        :returns: Boolean indicating message mention the client.
        """

        return self.event.hasme


    @property
    def whome(
        self,
    ) -> tuple[str, str] | None:
        """
        Return the current nickname of the client on the server.

        :returns: Current nickname of the client on the server.
        """

        return self.event.whome


    @property
    def author(
        self,
    ) -> tuple[str, str] | None:
        """
        Return the current nickname of the client on the server.

        :returns: Current nickname of the client on the server.
        """

        return self.event.author


    @property
    def anchor(
        self,
    ) -> str | None:
        """
        Return the unique value for the context with the client.

        :returns: Unique value for the context with the client.
        """

        kind = self.kind
        author = self.author
        event = self.event

        recipient = (
            event.recipient)

        if (recipient is None
                or author is None):
            return None

        return (
            ':'.join([
                str(x) for x
                in recipient])
            if kind == 'chanmsg'
            else author[1])


    @property
    def message(
        self,
    ) -> str | None:
        """
        Return the string containing the content of the message.

        :returns: String containing the content of the message.
        """

        return self.event.message


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
