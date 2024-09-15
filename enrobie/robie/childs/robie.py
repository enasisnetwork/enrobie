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
from .plugin import RobiePlugin

if TYPE_CHECKING:
    from ..robie import Robie



RobieClients = dict[str, RobieClient]
RobiePlugins = dict[str, RobiePlugin]



class RobieChilds:
    """
    Contain the object instances for related Robie children.

    :param robie: Primary class instance for Chatting Robie.
    """

    __robie: 'Robie'

    __clients: RobieClients
    __plugins: RobiePlugins


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

        robie.logger.log_i(
            base=self,
            status='created')


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

            if not params.enable:
                return NCNone

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

            if not params.enable:
                return NCNone

            object = plugin(
                robie, name, params)

            target[name] = object


        if plugin is not None:
            _put_plugin()
