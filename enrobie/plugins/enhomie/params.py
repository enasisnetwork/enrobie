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
from ...robie.params import RobiePluginParams
from ...robie.params.common import RobieParamsModel



class HomiePluginCommandParams(RobieParamsModel, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    irc: Annotated[
        str,
        Field('!persist',
              description='Command name for chat platform',
              min_length=2)]

    dsc: Annotated[
        str,
        Field('!persist',
              description='Command name for chat platform',
              min_length=2)]

    mtm: Annotated[
        str,
        Field('!persist',
              description='Command name for chat platform',
              min_length=2)]



class HomiePluginParams(RobiePluginParams, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    command: Annotated[
        HomiePluginCommandParams,
        Field(default_factory=HomiePluginCommandParams,
              description='Command name per chat platform')]

    restful: Annotated[
        str,
        Field(...,
              description='Where to find the RESTful API',
              examples=['http://localhost:8420'],
              min_length=1)]

    username: Annotated[
        Optional[str],
        Field(None,
              description='Authenticate with the service',
              min_length=1)]

    password: Annotated[
        Optional[str],
        Field(None,
              description='Authenticate with the service',
              min_length=1)]

    timeout: Annotated[
        int,
        Field(30,
              description='Timeout connecting to server',
              ge=1, le=300)]

    ssl_verify: Annotated[
        bool,
        Field(True,
              description='Verify the ceritifcate valid')]

    ssl_capem: Annotated[
        Optional[str],
        Field(None,
              description='Verify the ceritifcate valid',
              min_length=1)]

    clients: Annotated[
        list[str],
        Field(...,
              description='List of clients to enable plugin',
              min_length=1)]

    trusted: Annotated[
        Optional[list[str]],
        Field(None,
              description='Users are trusted by the plugin',
              min_length=1)]

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
                'restful',
                'username',
                'password',
                'timeout',
                'ssl_verify',
                'ssl_capem',
                'status']

            for key in parsable:

                value = data.get(key)

                if value is None:
                    continue

                value = _parse(value)

                data[key] = value


        super().__init__(**data)
