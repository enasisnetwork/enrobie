"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from contextlib import suppress
from typing import Optional
from typing import Type

from encommon.config import Config
from encommon.config import Params
from encommon.types import DictStrAny
from encommon.utils.common import PATHABLE

from .params import RobieClientParams
from .params import RobieParams
from .params import RobiePluginParams



class RobieConfig(Config):
    """
    Contain the configurations from the arguments and files.

    :param sargs: Additional arguments on the command line.
    :param files: Complete or relative path to config files.
    :param cargs: Configuration arguments in dictionary form,
        which will override contents from the config files.
    """

    __clients: dict[str, Type[RobieClientParams]]
    __plugins: dict[str, Type[RobiePluginParams]]


    def __init__(
        self,
        sargs: Optional[DictStrAny] = None,
        files: Optional[PATHABLE] = None,
        cargs: Optional[DictStrAny] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        sargs = dict(sargs or {})
        cargs = dict(cargs or {})

        self.__clients = {}
        self.__plugins = {}


        _console = (
            sargs.get('console'))

        _debug = (
            sargs.get('debug'))

        key = 'enlogger/stdo_level'

        if _console is True:
            cargs[key] = 'info'

        if _debug is True:
            cargs[key] = 'debug'


        if 'config' in sargs:
            files = sargs['config']


        _pmessage = (
            sargs.get('pmessage'))

        _pcommand = (
            sargs.get('pcommand'))

        if _pmessage is not None:
            key = 'printer/message'
            cargs[key] = _pmessage

        if _pcommand is not None:
            key = 'printer/command'
            cargs[key] = _pcommand


        super().__init__(
            files=files,
            cargs=cargs,
            sargs=sargs,
            model=RobieParams)


    @property
    def params(
        self,
    ) -> RobieParams:
        """
        Return the Pydantic model containing the configuration.

        .. warning::
           This method completely overrides the parent but is
           based on that code, would be unfortunate if upstream
           changes meant this breaks or breaks something else.

        :returns: Pydantic model containing the configuration.
        """

        params = self.__params

        if params is not None:

            assert isinstance(
                params, RobieParams)

            return params


        basic = self.basic
        update = False

        with suppress(AttributeError):
            basic = self.merge
            update = True


        _clients = basic.get('clients')
        _plugins = basic.get('plugins')


        def _put_clients() -> None:

            models = self.__clients
            target = basic['clients']

            items = target.items()

            for name, params in items:

                model = models[name]
                object = model(**params)

                target[name] = object


        if _clients is not None:
            _put_clients()


        def _put_plugins() -> None:

            models = self.__plugins
            target = basic['plugins']

            items = target.items()

            for name, params in items:

                model = models[name]
                object = model(**params)

                target[name] = object


        if _plugins is not None:
            _put_plugins()


        params = (
            self.model(**basic))

        assert isinstance(
            params, RobieParams)


        if update is True:
            self.__params = params

        return params


    @property
    def __params(
        self,
    ) -> Optional[Params]:
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self._Config__params


    @__params.setter
    def __params(
        self,
        value: Params,
    ) -> None:
        """
        Update the value for the attribute from class instance.
        """

        self._Config__params = value


    @property
    def config(
        self,
    ) -> DictStrAny:
        """
        Return the configuration dumped from the Pydantic model.

        .. warning::
           This method completely overrides the parent but is
           based on that code, would be unfortunate if upstream
           changes meant this breaks or breaks something else.

        :returns: Configuration dumped from the Pydantic model.
        """

        params = self.params

        _clients = params.clients
        _plugins = params.plugins

        config = params.endumped


        def _get_clients() -> None:

            target = config['clients']

            assert _clients is not None

            items = _clients.items()

            for name, client in items:
                target[name] = (
                    client.endumped)


        if _clients is not None:
            _get_clients()


        def _get_plugins() -> None:

            target = config['plugins']

            assert _plugins is not None

            items = _plugins.items()

            for name, plugin in items:
                target[name] = (
                    plugin.endumped)


        if _plugins is not None:
            _get_plugins()


        return config


    def register(
        self,
        name: str,
        *,
        client: Optional[Type[RobieClientParams]] = None,
        plugin: Optional[Type[RobiePluginParams]] = None,
    ) -> None:
        """
        Register the plugin parameters for parameter processing.

        :param name: Name of the object within the Robie config.
        :param client: Class definition for the instantiation.
        :param plugin: Class definition for the instantiation.
        """

        clients = self.__clients
        plugins = self.__plugins

        if client is not None:
            clients[name] = client

        if plugin is not None:
            plugins[name] = plugin
