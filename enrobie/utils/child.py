"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING
from typing import Union

if TYPE_CHECKING:
    from ..robie.childs import RobieChild



_PHASE = Literal[
    'initial',
    'runtime']



class InvalidChild(Exception):
    """
    Exception for when the child could not be instantiated.

    .. note::
       Similar or identical to classes in other projects.

    :param child: Name or child that is determined invalid.
    :param phase: From which phase child was found invalid.
    :param about: Additional information for the exception.
    """

    child: str
    phase: _PHASE
    about: Optional[str] = None


    def __init__(
        self,
        child: Union[str, 'RobieChild'],
        phase: _PHASE,
        about: Optional[str] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        if hasattr(child, 'name'):
            child = child.name

        message = (
            f'Child ({child}) '
            'invalid within '
            f'phase ({phase})')

        if about is not None:
            message += (
                f' ({about})')

        self.child = child
        self.about = about

        super().__init__(message)
