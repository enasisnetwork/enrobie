"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Literal
from typing import TYPE_CHECKING

from ...robie.models import RobieCommand

if TYPE_CHECKING:
    from ...robie.childs import RobieClient



@dataclass
class IRCCommand(RobieCommand):
    """
    Contain information for sharing using the Python queue.
    """

    event: str


    def __init__(
        self,
        client: 'RobieClient',
        event: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        # Translate to client.command

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
