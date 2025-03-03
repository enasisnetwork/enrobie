"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.parse import Jinja2
from encommon.parse.jinja2 import FILTERS
from encommon.types import DictStrAny

if TYPE_CHECKING:
    from ..robie import Robie



class RobieJinja2(Jinja2):
    """
    Parse the provided input and intelligently return value.

    :param robie: Primary class instance for Chatting Robie.
    """


    def __init__(
        self,
        robie: 'Robie',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        statics: DictStrAny = {
            'robie': robie}

        filters: FILTERS = {}

        super().__init__(
            statics=statics,
            filters=filters)
