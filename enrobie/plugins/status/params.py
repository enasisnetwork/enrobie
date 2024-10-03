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


from ...robie.params import RobiePluginParams
from ...robie.params.common import RobieParamsModel



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



class StatusPluginParams(RobiePluginParams, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    command: Annotated[
        StatusPluginCommandParams,
        Field(default_factory=StatusPluginCommandParams,
              description='Command name per chat platform')]


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

            parsable = ['command']

            for key in parsable:

                value = data.get(key)

                if value is None:
                    continue

                value = _parse(value)

                data[key] = value


        super().__init__(**data)