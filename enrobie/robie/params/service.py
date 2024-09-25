"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated

from pydantic import Field

from .common import RobieParamsModel



class RobieServiceRespiteParams(RobieParamsModel, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    health: Annotated[
        int,
        Field(3,
              description='How often health is checked',
              ge=1, le=15)]



class RobieServiceParams(RobieParamsModel, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    respite: Annotated[
        RobieServiceRespiteParams,
        Field(default_factory=RobieServiceRespiteParams,
              description='When operates are performed')]
