"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Callable
from typing import Optional

from enconnect.irc import ClientParams

from pydantic import Field

from ...plugins import StatusPluginIconParams
from ...robie.params import RobieClientParams



class IRCClientParams(RobieClientParams, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    client: Annotated[
        ClientParams,
        Field(...,
              description='Parameters for the base client')]

    delay: Annotated[
        int,
        Field(15,
              description='Period to wait for reconnect',
              ge=1, le=300)]

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
                'client',
                'delay',
                'status']

            for key in parsable:

                value = data.get(key)

                if value is None:
                    continue

                value = _parse(value)

                data[key] = value


        super().__init__(**data)
