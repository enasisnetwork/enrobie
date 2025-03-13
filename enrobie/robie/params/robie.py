"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Callable
from typing import Optional

from encommon.config import Params

from pydantic import Field

from .client import RobieClientParams
from .common import RobieParamsModel
from .person import RobiePersonParams
from .plugin import RobiePluginParams
from .service import RobieServiceParams



class RobiePrinterParams(RobieParamsModel, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    message: Annotated[
        bool,
        Field(False,
              description='Print the messages to console')]

    command: Annotated[
        bool,
        Field(False,
              description='Print the commands to console')]



class RobieParams(Params, extra='forbid'):
    """
    Process and validate the core configuration parameters.
    """

    database: Annotated[
        str,
        Field('sqlite:///:memory:',
              description='Database connection string',
              min_length=1)]

    printer: Annotated[
        RobiePrinterParams,
        Field(default_factory=RobiePrinterParams,
              description='Print messages to console')]

    service: Annotated[
        RobieServiceParams,
        Field(default_factory=RobieServiceParams,
              description='Parameters for Robie Service')]

    clients: Annotated[
        Optional[dict[str, RobieClientParams]],
        Field(None,
              description='Parameters for Robie clients',
              min_length=1)]

    plugins: Annotated[
        Optional[dict[str, RobiePluginParams]],
        Field(None,
              description='Parameters for Robie plugins',
              min_length=1)]

    persons: Annotated[
        Optional[dict[str, RobiePersonParams]],
        Field(None,
              description='Parameters for Robie persons',
              min_length=1)]


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

            parsable = ['persons']

            for key in parsable:

                if not data.get(key):
                    continue

                values = (
                    data[key]
                    .values())

                for item in values:
                    item['_parse'] = _parse


        if _parse is not None:

            parsable = [
                'database',
                'printer',
                'service']

            for key in parsable:

                value = data.get(key)

                if value is None:
                    continue

                value = _parse(value)

                data[key] = value


        super().__init__(**data)
