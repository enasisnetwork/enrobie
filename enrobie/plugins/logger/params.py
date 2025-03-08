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



class LoggerPluginParams(RobiePluginParams, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    database: Annotated[
        str,
        Field('sqlite:///:memory:',
              description='Database connection string',
              min_length=1)]

    histories: Annotated[
        int,
        Field(100,
              description='Number of messages per anchor',
              ge=1, le=10000)]

    clients: Annotated[
        list[str],
        Field(...,
              description='List of clients to enable plugin',
              min_length=1)]

    output: Annotated[
        Optional[str],
        Field(None,
              description='Optional path where logs append',
              min_length=4)]

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
                'database',
                'histories',
                'clients',
                'output',
                'status']

            for key in parsable:

                value = data.get(key)

                if value is None:
                    continue

                value = _parse(value)

                data[key] = value


        super().__init__(**data)
