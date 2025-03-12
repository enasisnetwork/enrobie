"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from ..addons import RobieQueueItem

if TYPE_CHECKING:
    from ..childs import RobieClient
    from ..childs import RobiePerson
    from ..models import RobieCommand
    from ..robie import Robie



RobieMessageKinds = Literal[
    'event',
    'chanmsg',
    'privmsg']



@dataclass
class RobieMessage(RobieQueueItem):
    """
    Contain information for sharing using the Python queue.
    """

    client: str
    person: Optional[str]


    def __init__(
        self,
        client: 'RobieClient',
        person: Optional['RobiePerson'] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.client = client.name

        self.person = (
            person.name
            if person is not None
            else None)

        super().__init__()


    @property
    def family(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        raise NotImplementedError


    @property
    def kind(
        self,
    ) -> 'RobieMessageKinds':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        raise NotImplementedError


    @property
    def isme(
        self,
    ) -> bool:
        """
        Return the boolean indicating message origin from client.

        :returns: Boolean indicating message origin from client.
        """

        raise NotImplementedError


    @property
    def hasme(
        self,
    ) -> bool:
        """
        Return the boolean indicating message mention the client.

        :returns: Boolean indicating message mention the client.
        """

        raise NotImplementedError


    @property
    def whome(
        self,
    ) -> tuple[str, str] | None:
        """
        Return the current nickname of the client on the server.

        :returns: Current nickname of the client on the server.
        """

        raise NotImplementedError


    @property
    def author(
        self,
    ) -> tuple[str, str] | None:
        """
        Return the current nickname of the client on the server.

        :returns: Current nickname of the client on the server.
        """

        raise NotImplementedError


    @property
    def anchor(
        self,
    ) -> str | None:
        """
        Return the unique value for the context with the client.

        :returns: Unique value for the context with the client.
        """

        raise NotImplementedError


    @property
    def message(
        self,
    ) -> str | None:
        """
        Return the string containing the content of the message.

        :returns: String containing the content of the message.
        """

        raise NotImplementedError


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

        raise NotImplementedError
