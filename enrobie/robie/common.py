"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import TYPE_CHECKING
from typing import Union

from encommon.utils.stdout import ANSIARRAY

if TYPE_CHECKING:
    from .childs.client import RobieClient
    from .childs.plugin import RobiePlugin
    from .threads.thread import RobieThreadItems



RobieKinds = Literal[
    'client',
    'plugin',
    'person']

RobiePrint = Union[
    ANSIARRAY,
    'RobieThreadItems']

RobieOperate = Union[
    'RobieClient',
    'RobiePlugin']
