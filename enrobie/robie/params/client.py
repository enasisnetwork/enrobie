"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Callable
from typing import Optional

from pydantic import Field

from .child import RobieChildParams



class RobieClientParams(RobieChildParams, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    locate: Annotated[
        Optional[str],
        Field(None,
              description='For which client are parameters',
              examples=[
                  'enrobie.clients.DSCClient',
                  'enrobie.clients.IRCClient',
                  'enrobie.clients.MTMClient'],
              min_length=1)]


    def __init__(
        # NOCVR
        self,
        /,
        _parse: Optional[Callable[..., Any]] = None,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(**data)
