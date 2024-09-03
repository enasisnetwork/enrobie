"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated

from encommon.types import BaseModel

from pydantic import Field



class RobieChildParams(BaseModel, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    enable: Annotated[
        bool,
        Field(False,
              description='Determine whether plugin enabled')]
