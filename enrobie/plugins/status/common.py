"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Literal
from typing import TYPE_CHECKING

from encommon.times import Time

if TYPE_CHECKING:
    from .params import StatusPluginIconParams



StatusPluginStates = Literal[
    'pending',
    'normal',
    'failure',
    'unknown']



@dataclass
class StatusPluginItem:
    """
    Contain the relevant status information for the entry.
    """

    time: Time
    unique: str
    group: str
    title: str
    icon: 'StatusPluginIconParams'
    state: StatusPluginStates


    def __lt__(
        self,
        other: 'StatusPluginItem',
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        .. note::
           Useful with sorting to influence consistent output.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        unique = self.unique
        _unique = other.unique

        return unique < _unique



StatusPluginItems = dict[
    str, StatusPluginItem]
