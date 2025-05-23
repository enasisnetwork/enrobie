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



class AutoNickPluginServiceParams(RobieParamsModel, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    client: Annotated[
        str,
        Field(...,
              description='Client where services exist',
              min_length=1)]

    password: Annotated[
        str,
        Field(...,
              description='Identify with nick services',
              min_length=1)]

    service: Annotated[
        str,
        Field('NickServ',
              description='Nickname of network service',
              min_length=1)]



class AutoNickPluginParams(RobiePluginParams, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    clients: Annotated[
        list[str],
        Field(...,
              description='List of clients to enable plugin',
              min_length=1)]

    interval: Annotated[
        int,
        Field(5,
              description='Interval when nick is validated',
              ge=5, le=300)]

    services: Annotated[
        Optional[list[AutoNickPluginServiceParams]],
        Field(None,
              description='How to identify with services')]

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


        clients = data.get('clients')

        if isinstance(clients, str):
            data['clients'] = [clients]


        if _parse is not None:

            parsable = [
                'clients',
                'interval',
                'status']

            for key in parsable:

                value = data.get(key)

                if value is None:
                    continue

                value = _parse(value)

                data[key] = value


        super().__init__(**data)
