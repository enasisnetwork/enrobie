"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Annotated
from typing import Any
from typing import Callable
from typing import Optional
from typing import TYPE_CHECKING

from encommon.types import BaseModel

from pydantic import Field

if TYPE_CHECKING:
    from .plugin import AinswerPlugin
    from ...robie.models import RobieMessage



AinswerIgnored = 'no_response'

AinswerTool = Callable[..., Any]



@dataclass
class AinswerDepends:
    """
    Dependencies related to operation with PydanticAI tools.
    """

    plugin: 'AinswerPlugin'
    mitem: Optional['RobieMessage']



class AinswerResponse(BaseModel, extra='forbid'):
    """
    Contains the response for question for the client type.
    """

    text: Annotated[
        str,
        Field(...,
              description='Simple and concise format.')]



class AinswerResponseDSC(AinswerResponse, extra='forbid'):
    """
    Contains the response for question for the client type.
    """

    text: Annotated[
        str,
        Field(...,
              description='Format intended for Discord.',
              max_length=1900)]



class AinswerResponseIRC(AinswerResponse, extra='forbid'):
    """
    Contains the response for question for the client type.
    """

    text: Annotated[
        str,
        Field(...,
              description='Format intended for IRCv2.',
              max_length=350)]



class AinswerResponseMTM(AinswerResponse, extra='forbid'):
    """
    Contains the response for question for the client type.
    """

    text: Annotated[
        str,
        Field(...,
              description='Format intended for Mattermost.',
              max_length=1900)]
