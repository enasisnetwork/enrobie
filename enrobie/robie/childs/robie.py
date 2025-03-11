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

from .client import RobieClient
from .person import RobiePerson
from .plugin import RobiePlugin

if TYPE_CHECKING:
    from ..robie import Robie



RobieClients = dict[str, RobieClient]
RobiePlugins = dict[str, RobiePlugin]
RobiePersons = dict[str, RobiePerson]



class RobieChilds:
    """
    Contain the object instances for related Robie children.

    :param robie: Primary class instance for Chatting Robie.
    """

    __robie: 'Robie'

    __clients: RobieClients
    __plugins: RobiePlugins
    __persons: RobiePersons


    def __init__(
        self,
        robie: 'Robie',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        robie.logger.log_d(
            base=self,
            status='initial')

        self.__robie = robie

        self.__clients = {}
        self.__plugins = {}
        self.__persons = {}

        self.build_objects()

        robie.logger.log_i(
            base=self,
            status='created')


    def build_objects(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        self.__build_persons()


    def __build_persons(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        robie = self.__robie
        params = robie.params
        persons = params.persons

        if persons is None:
            return None

        model = RobiePerson


        childs: RobiePersons = {}


        items = persons.items()

        for name, person in items:

            object = model(
                robie, name, person)

            childs[name] = object


        self.__persons = childs


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """


        clients = (
            self.__clients
            .values())

        for client in clients:
            client.validate()


        plugins = (
            self.__plugins
            .values())

        for plugin in plugins:
            plugin.validate()


        persons = (
            self.__persons
            .values())

        for person in persons:
            person.validate()


    @property
    def clients(
        self,
    ) -> RobieClients:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        clients = self.__clients

        return dict(clients)


    @property
    def plugins(
        self,
    ) -> RobiePlugins:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        plugins = self.__plugins

        return dict(plugins)


    @property
    def persons(
        self,
    ) -> RobiePersons:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        persons = self.__persons

        return dict(persons)


    @property
    def dumped(
        self,
    ) -> DictStrAny:
        """
        Return the facts about the attributes from the instance.

        :returns: Facts about the attributes from the instance.
        """

        clients = self.clients
        plugins = self.plugins

        dumped: DictStrAny = {

            'clients': {
                k: v.dumped for k, v
                in clients.items()},

            'plugins': {
                k: v.dumped for k, v
                in plugins.items()}}

        return deepcopy(dumped)


    def register(  # noqa: CFQ004
        self,
        name: str,
        *,
        client: Optional[Type[RobieClient]] = None,
        plugin: Optional[Type[RobiePlugin]] = None,
    ) -> None:
        """
        Register the plugin with the internal operation routine.

        :param name: Name of the object within the Robie config.
        :param client: Class definition for the instantiation.
        :param plugin: Class definition for the instantiation.
        """

        robie = self.__robie
        params = robie.params

        _clients = params.clients
        _plugins = params.plugins


        def _put_client() -> None:

            target = self.__clients

            if _clients is None:
                return NCNone

            if name not in _clients:
                return NCNone

            params = _clients[name]

            assert callable(client)

            object = client(
                robie, name, params)

            target[name] = object


        if client is not None:
            _put_client()


        def _put_plugin() -> None:

            target = self.__plugins

            if _plugins is None:
                return NCNone

            if name not in _plugins:
                return NCNone

            params = _plugins[name]

            assert callable(plugin)

            object = plugin(
                robie, name, params)

            target[name] = object


        if plugin is not None:
            _put_plugin()
