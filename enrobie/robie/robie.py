"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Optional
from typing import TYPE_CHECKING
from typing import Type

from encommon.types import DictStrAny
from encommon.types import NCNone
from encommon.types import clsname
from encommon.utils import array_ansi
from encommon.utils import print_ansi

from .addons import RobieLogger
from .childs import RobieChilds
from .models import RobieModels

if TYPE_CHECKING:
    from .common import RobiePrint
    from .config import RobieConfig
    from .childs import RobieClient
    from .childs import RobiePlugin
    from .params import RobieParams



class Robie:
    """
    Interact with chat networks and integrate using plugins.

    :param config: Primary class instance for configuration.
    """

    __config: 'RobieConfig'

    __logger: RobieLogger

    __childs: RobieChilds


    def __init__(
        self,
        config: 'RobieConfig',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        config.logger.log_d(
            base=clsname(self),
            status='initial')

        self.__config = config

        self.__logger = (
            RobieLogger(self))

        self.__childs = (
            RobieChilds(self))

        self.childs.validate()

        config.logger.log_d(
            base=clsname(self),
            status='created')


    @property
    def config(
        self,
    ) -> 'RobieConfig':
        """
        Return the Config instance containing the configuration.

        :returns: Config instance containing the configuration.
        """

        return self.__config


    @property
    def logger(
        self,
    ) -> RobieLogger:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__logger


    @property
    def childs(
        self,
    ) -> RobieChilds:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__childs


    @property
    def params(
        self,
    ) -> 'RobieParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.config.params


    def printer(
        self,
        source: 'RobiePrint',
        color: int = 6,
    ) -> None:
        """
        Print the contents for the object within Robie instance.

        :param source: Content which will be shown after header.
        :param color: Override the color used for box character.
        """

        params = self.params
        printer = params.printer

        pmessage = printer.message
        pcommand = printer.command


        RobieMessage = (
            RobieModels
            .message())

        RobieCommand = (
            RobieModels
            .command())


        message = isinstance(
            source, RobieMessage)

        if message and not pmessage:
            return NCNone


        command = isinstance(
            source, RobieCommand)

        if command and not pcommand:
            return NCNone


        print_ansi(
            f'\n<c9{color}>┍'
            f'{"━" * 63}<c0>')

        dumped = array_ansi(
            source, indent=2)

        print(  # noqa: T201
            f'\n{dumped}')

        print_ansi(
            f'\n<c9{color}>┕'
            f'{"━" * 63}<c0>\n')


    @property
    def dumped(
        self,
    ) -> DictStrAny:
        """
        Return the facts about the attributes from the instance.

        :returns: Facts about the attributes from the instance.
        """

        params = deepcopy(
            self.params.endumped)

        childs = deepcopy(
            self.childs.dumped)

        items = childs.items()

        for key, value in items:
            params[key] = value

        return params


    def register(
        self,
        name: str,
        *,
        client: Optional[Type['RobieClient']] = None,
        plugin: Optional[Type['RobiePlugin']] = None,
    ) -> None:
        """
        Register the plugin with the internal operation routine.

        :param name: Name of the object within the Robie config.
        :param client: Class definition for the instantiation.
        :param plugin: Class definition for the instantiation.
        """

        self.childs.register(
            name=name,
            client=client,
            plugin=plugin)
