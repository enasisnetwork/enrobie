"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Literal

from encommon.times import Time

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
    icon: StatusPluginIconParams
    state: StatusPluginStates
