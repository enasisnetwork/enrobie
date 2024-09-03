"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Literal
from typing import TYPE_CHECKING

from ..addons import RobieQueueItem

if TYPE_CHECKING:
    from ..childs import RobieClient
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


    def __init__(
        self,
        client: 'RobieClient',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.client = client.name

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
