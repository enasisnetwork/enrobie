"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING
from typing import Type
from typing import Union

from .child import RobieChild
from .person import RobiePerson
from ..models import RobieMessage
from ..models import RobieModels

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
    def params(
        self,
    ) -> 'RobiePluginParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            RobieModels
            .plugin())

        params = super().params

        assert isinstance(
            params, model)

        return params


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


    def trusted(
        self,
        check: Union[str, RobiePerson, RobieMessage],
    ) -> bool:
        """
        Return the boolean indicating whether person is trusted.

        :param check: Validate the person is trusted by plugin.
        :returns: Boolean indicating whether person is trusted.
        """

        params = self.params
        trusted = params.trusted

        if trusted is None:
            return True

        if isinstance(check, RobieMessage):

            if not check.person:
                return False

            check = check.person

        elif isinstance(check, RobiePerson):
            check = check.name

        return check in trusted


    def notrust(
        self,
        check: Union[str, RobiePerson, RobieMessage],
    ) -> bool:
        """
        Return the boolean indicating whether person is trusted.

        :param check: Validate the person is trusted by plugin.
        :returns: Boolean indicating whether person is trusted.
        """

        return not self.trusted(check)
