"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Callable
from typing import Optional

from encommon.types import BaseModel

from pydantic import Field

from .common import StatusPluginStates
from ...robie.params import RobiePluginParams
from ...robie.params.common import RobieParamsModel



class StatusPluginReportParams(BaseModel, extra='forbid'):
    """
    Contain information for constructing the chat messages.
    """

    client: Annotated[
        str,
        Field(...,
              description='Client where channel exists',
              min_length=1)]

    target: Annotated[
        str,
        Field(...,
              description='Where message will be sent',
              min_length=1)]

    states: Annotated[
        Optional[list[StatusPluginStates]],
        Field(None,
              description='Where message will be sent',
              min_length=1)]


    def __init__(
        # NOCVR
        self,
        /,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        states = data.get('states')

        if isinstance(states, str):
            data['states'] = [states]

        super().__init__(**data)



class StatusPluginCommandParams(RobieParamsModel, extra='forbid'):
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



class StatusPluginIconParams(BaseModel, extra='forbid'):
    """
    Contain information for constructing the chat messages.
    """

    irc: Annotated[
        Optional[str],
        Field(None,
              description='Icon used for the chat platform',
              min_length=1)]

    dsc: Annotated[
        Optional[str],
        Field(None,
              description='Icon used for the chat platform',
              min_length=1)]

    mtm: Annotated[
        Optional[str],
        Field(None,
              description='Icon used for the chat platform',
              min_length=1)]



class StatusPluginIconsParams(BaseModel, extra='forbid'):
    """
    Contain information for constructing the chat messages.
    """

    pending: Annotated[
        StatusPluginIconParams,
        Field(default_factory=StatusPluginIconParams,
              description='Icon used per the chat platform')]

    normal: Annotated[
        StatusPluginIconParams,
        Field(default_factory=StatusPluginIconParams,
              description='Icon used per the chat platform')]

    failure: Annotated[
        StatusPluginIconParams,
        Field(default_factory=StatusPluginIconParams,
              description='Icon used per the chat platform')]

    unknown: Annotated[
        StatusPluginIconParams,
        Field(default_factory=StatusPluginIconParams,
              description='Icon used per the chat platform')]



class StatusPluginParams(RobiePluginParams, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    reports: Annotated[
        Optional[list[StatusPluginReportParams]],
        Field(None,
              description='Where to send status updates',
              min_length=1)]

    command: Annotated[
        StatusPluginCommandParams,
        Field(default_factory=StatusPluginCommandParams,
              description='Command name per chat platform')]

    icons: Annotated[
        StatusPluginIconsParams,
        Field(default_factory=StatusPluginIconsParams,
              description='Icon used per the chat platform')]


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


        if _parse is not None:

            parsable = [
                'report',
                'command',
                'icons']

            for key in parsable:

                value = data.get(key)

                if value is None:
                    continue

                value = _parse(value)

                data[key] = value


        super().__init__(**data)
