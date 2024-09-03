"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from enconnect.utils.http import _METHODS
from enconnect.utils.http import _PAYLOAD

from ...robie.models import RobieCommand

if TYPE_CHECKING:
    from ...robie.childs import RobieClient



@dataclass
class DSCCommand(RobieCommand):
    """
    Contain information for sharing using the Python queue.
    """

    method: _METHODS
    path: str
    params: Optional[_PAYLOAD]
    json: Optional[_PAYLOAD]


    def __init__(
        self,
        client: 'RobieClient',
        method: _METHODS,
        path: str,
        params: Optional[_PAYLOAD] = None,
        json: Optional[_PAYLOAD] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        # Translate to client.request

        self.method = method
        self.path = path
        self.params = params
        self.json = json

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
