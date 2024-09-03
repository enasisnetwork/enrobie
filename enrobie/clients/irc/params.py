"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated

from enconnect.irc import ClientParams

from pydantic import Field

from ...robie.params import RobieClientParams



class IRCClientParams(RobieClientParams, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    client: Annotated[
        ClientParams,
        Field(...,
              description='Parameters for the base client')]
