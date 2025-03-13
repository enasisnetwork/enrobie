"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import DictStrAny

if TYPE_CHECKING:
    from ..common import RobieKinds
    from ..params import RobieChildParams
    from ..robie import Robie



class RobieChild:
    """
    Parent object for child objects within the project base.

    :param robie: Primary class instance for Chatting Robie.
    :param name: Name of the object within the Robie config.
    :param params: Parameters used to instantiate the class.
    """

    __robie: 'Robie'

    __name: str
    __params: 'RobieChildParams'


    def __init__(
        self,
        robie: 'Robie',
        name: str,
        params: 'RobieChildParams',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        robie.logger.log_d(
            base=self,
            name=name,
            status='initial')

        self.__robie = robie
        self.__name = name
        self.__params = params

        self.__post__()

        robie.logger.log_d(
            base=self,
            name=name,
            status='created')


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        raise NotImplementedError


    def __lt__(
        self,
        other: 'RobieChild',
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        .. note::
           Useful with sorting to influence consistent output.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        name = self.name
        _name = other.name

        return name < _name


    @property
    def robie(
        self,
    ) -> 'Robie':
        """
        Return the Robie instance to which the instance belongs.

        :returns: Robie instance to which the instance belongs.
        """

        return self.__robie


    @property
    def enable(
        self,
    ) -> bool:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.params.enable


    @property
    def name(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__name


    @property
    def kind(
        self,
    ) -> 'RobieKinds':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        raise NotImplementedError


    @property
    def params(
        self,
    ) -> 'RobieChildParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    @property
    def dumped(
        self,
    ) -> DictStrAny:
        """
        Return the facts about the attributes from the instance.

        :returns: Facts about the attributes from the instance.
        """

        params = self.__params
        dumped = params.endumped

        return {
            'name': self.name,
            'kind': self.kind,
            'params': dumped}
