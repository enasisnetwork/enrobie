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

from .child import RobieChildParams
from .common import RobieParamsModel



class RobiePersonMatchParams(RobieParamsModel, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    client: Annotated[
        str,
        Field(...,
              description='Client where the user exists',
              min_length=1)]

    match: Annotated[
        list[str],
        Field(...,
              description='Values client uses to identify',
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

        match = data.get('match')

        if isinstance(match, str):
            data['match'] = [match]

        super().__init__(**data)



class RobiePersonParams(RobieChildParams, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """

    first: Annotated[
        Optional[str],
        Field(None,
              description='Additional optional information',
              min_length=1)]

    last: Annotated[
        Optional[str],
        Field(None,
              description='Additional optional information',
              min_length=1)]

    about: Annotated[
        Optional[str],
        Field(None,
              description='Additional optional information',
              min_length=1)]

    matches: Annotated[
        list[RobiePersonMatchParams],
        Field(...,
              description='How the user will be identified')]

    weight: Annotated[
        int,
        Field(50,
              description='Determine order of precedence',
              ge=1, le=100)]


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
                'first',
                'last',
                'about',
                'matches',
                'weight']

            for key in parsable:

                value = data.get(key)

                if value is None:
                    continue

                value = _parse(value)

                data[key] = value


        super().__init__(**data)
