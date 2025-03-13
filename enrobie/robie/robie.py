"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Any
from typing import Optional
from typing import TYPE_CHECKING
from typing import Type

from encommon.types import DictStrAny
from encommon.types import NCNone
from encommon.types import clsname
from encommon.utils import array_ansi
from encommon.utils import print_ansi

from .addons import RobieJinja2
from .addons import RobieLogger
from .childs import RobieChilds
from .childs import RobieClient
from .childs import RobiePlugin
from .models import RobieModels
from ..utils import importer

if TYPE_CHECKING:
    from .common import RobiePrint
    from .config import RobieConfig
    from .params import RobieParams
    from .childs import RobiePerson



class Robie:
    """
    Interact with chat networks and integrate using plugins.

    :param config: Primary class instance for configuration.
    """

    __config: 'RobieConfig'

    __logger: RobieLogger
    __jinja2: RobieJinja2

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

        self.__jinja2 = (
            RobieJinja2(self))

        self.__childs = (
            RobieChilds(self))

        self.childs.validate()

        config.logger.log_d(
            base=clsname(self),
            status='created')

        self.register_locate()


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
    def jinja2(
        self,
    ) -> RobieJinja2:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__jinja2


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


        line: str = '━'

        print_ansi(
            f'\n<c9{color}>┍'
            f'{line * 63}<c0>')

        dumped = array_ansi(
            source, indent=2)

        print(  # noqa: T201
            f'\n{dumped}')

        print_ansi(
            f'\n<c9{color}>┕'
            f'{line * 63}<c0>\n')


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


    def register_locate(
        self,
    ) -> None:
        """
        Register the plugin with the internal operation routine.
        """

        config = self.config
        merge = config.merge


        clients = (
            merge.get('clients')
            or {})

        items = clients.items()

        for name, source in items:

            locate = (
                source
                .get('locate'))

            if locate is None:
                continue  # NOCVR

            client = (
                importer(locate))

            assert issubclass(
                client,
                RobieClient)

            self.register(
                name=name,
                client=client)


        plugins = (
            merge.get('plugins')
            or {})

        items = plugins.items()

        for name, source in items:

            locate = (
                source
                .get('locate'))

            if locate is None:
                continue  # NOCVR

            plugin = (
                importer(locate))

            assert issubclass(
                plugin,
                RobiePlugin)

            self.register(
                name=name,
                plugin=plugin)


    def person(
        self,
        client: RobieClient,
        check: str,
    ) -> Optional['RobiePerson']:
        """
        Return the heaviest weighted match using provided check.

        :param client: Client class instance for Chatting Robie.
        :param check: Value to be searched within the haystack.
        :returns: Heaviest weighted match using provided check.
        """

        childs = self.childs

        persons = (
            childs.persons
            .values())


        matched: set['RobiePerson'] = set()


        for person in persons:

            if not person.enable:
                continue  # NOCVR

            match = person.match(
                client, check)

            if match is True:
                matched.add(person)


        if len(matched) == 0:
            return None

        ordered = sorted(
            matched,
            key=lambda x: x.weight,
            reverse=True)

        return ordered[0]


    def j2parse(
        self,
        value: Any,  # noqa: ANN401
        statics: Optional[DictStrAny] = None,
        literal: bool = True,
    ) -> Any:  # noqa: ANN401
        """
        Return the provided input using the Jinja2 environment.

        :param value: Input that will be processed and returned.
        :param statics: Additional values available for parsing.
        :param literal: Determine if Python objects are evaled.
        :returns: Provided input using the Jinja2 environment.
        """

        return self.__jinja2.parse(
            value, statics, literal)
