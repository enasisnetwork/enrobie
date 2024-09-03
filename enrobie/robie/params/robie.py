"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Optional

from encommon.config import Params
from encommon.types import BaseModel

from pydantic import Field

from .client import RobieClientParams
from .plugin import RobiePluginParams
from .service import RobieServiceParams



class RobiePrinterParams(BaseModel, extra='forbid'):
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
              description='Print the stream to console')]

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
