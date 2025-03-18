"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated

from encommon.types import BaseModel

from pydantic import Field



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
