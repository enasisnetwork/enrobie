"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING
from typing import Type

from .child import RobieChild

if TYPE_CHECKING:
    from ..params import RobiePluginParams
    from ..threads import RobiePluginThread



class RobiePlugin(RobieChild):
    """
    Integrate with the Robie routine and perform operations.
    """

    __thread: Optional['RobiePluginThread'] = None


    @property
    def kind(
        self,
    ) -> Literal['plugin']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'plugin'


    @classmethod
    def schema(
        cls,
    ) -> Type['RobiePluginParams']:
        """
        Return the configuration parameters relevant for class.

        :returns: Configuration parameters relevant for class.
        """

        raise NotImplementedError


    @property
    def thread(
        self,
    ) -> Optional['RobiePluginThread']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        from ..threads import (
            RobiePluginThread)

        thread = self.__thread

        if thread is None:
            return None

        assert isinstance(
            thread,
            RobiePluginThread)

        return thread


    @thread.setter
    def thread(
        self,
        value: 'RobiePluginThread',
    ) -> None:
        """
        Update the value for the attribute from class instance.
        """

        from ..threads import (
            RobiePluginThread)

        assert isinstance(
            value,
            RobiePluginThread)

        self.__thread = value


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service threads.

        .. note::
           Deviates from enhomie in children have operations,
           and are more isolated from internal core routines.
        """

        raise NotImplementedError
