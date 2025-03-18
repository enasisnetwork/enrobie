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

from ..status import StatusPluginIconParams
from ...robie.params import RobieParamsModel
from ...robie.params import RobiePluginParams



class AutoJoinPluginChannelParams(RobieParamsModel, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    client: Annotated[
        str,
        Field(...,
              description='Client where channel exists',
              min_length=1)]

    channel: Annotated[
        str,
        Field(...,
              description='Name of channel to remain joined',
              min_length=1)]



class AutoJoinPluginParams(RobiePluginParams, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    channels: Annotated[
        list[AutoJoinPluginChannelParams],
        Field(...,
              description='Which channels to maintain join',
              min_length=1)]

    interval: Annotated[
        int,
        Field(5,
              description='Interval when channels are joined',
              ge=5, le=300)]

    status: Annotated[
        StatusPluginIconParams,
        Field(default_factory=StatusPluginIconParams,
              description='Icon used per chat platform')]


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
                'channels',
                'interval',
                'status']

            for key in parsable:

                value = data.get(key)

                if value is None:
                    continue

                value = _parse(value)

                data[key] = value


        super().__init__(**data)
