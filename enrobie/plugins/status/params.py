"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated

from encommon.types import BaseModel

from pydantic import Field

from ...robie.params import RobiePluginParams



class StatusPluginCommandParams(BaseModel, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    irc: Annotated[
        str,
        Field('!status',
              description='Command name for chat platform')]

    dsc: Annotated[
        str,
        Field('!status',
              description='Command name for chat platform')]

    mtm: Annotated[
        str,
        Field('!status',
              description='Command name for chat platform')]



class StatusPluginParams(RobiePluginParams, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    command: Annotated[
        StatusPluginCommandParams,
        Field(default_factory=StatusPluginCommandParams,
              description='Command name per chat platform')]
