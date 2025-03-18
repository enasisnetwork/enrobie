"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from re import IGNORECASE
from re import compile
from re import match as re_match
from typing import TYPE_CHECKING
from typing import Type

from encommon.times import Timer
from encommon.types import NCFalse
from encommon.types import NCNone
from encommon.types.strings import SPACED

from .params import AutoNickPluginParams
from .params import AutoNickPluginServiceParams
from ..status import StatusPlugin
from ..status import StatusPluginStates
from ...robie.childs import RobiePlugin

if TYPE_CHECKING:
    from ...clients.irc import IRCClient
    from ...clients.irc.message import IRCMessage



_IDENTIFY = compile(
    r'this nick(name)? is registered',
    IGNORECASE)

_SERVICES = dict[str, AutoNickPluginServiceParams]



class AutoNickPlugin(RobiePlugin):
    """
    Integrate with the Robie routine and perform operations.

    .. note::
       This plugin maintains configured nickname on server.
    """

    __started: bool

    __nickserv: _SERVICES

    __timer: Timer


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__started = False

        params = self.params


        nickserv: _SERVICES = {}

        if params.services:

            services = params.services

            for service in services:

                name = service.client

                nickserv[name] = service

        self.__nickserv = nickserv


        self.__timer = Timer(
            params.interval)

        self.__status('pending')


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        # Review the parameters


    @classmethod
    def schema(
        cls,
    ) -> Type[AutoNickPluginParams]:
        """
        Return the configuration parameters relevant for class.

        :returns: Configuration parameters relevant for class.
        """

        return AutoNickPluginParams


    @property
    def params(
        self,
    ) -> AutoNickPluginParams:
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        params = super().params

        assert isinstance(
            params,
            AutoNickPluginParams)

        return params


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service threads.
        """

        from ...clients.irc.message import IRCMessage

        assert self.thread

        thread = self.thread
        mqueue = thread.mqueue
        timer = self.__timer

        clients = (
            thread.service
            .clients.childs)


        if not self.__started:
            self.__started = True
            self.__status('normal')


        if timer.ready():
            self.__operate()


        while not mqueue.empty:

            mitem = mqueue.get()

            name = mitem.client
            family = mitem.family

            # Ignore unrelated clients
            if family != 'irc':
                continue

            assert isinstance(
                mitem, IRCMessage)

            # Ignore disabled clients
            if name not in clients:
                continue  # NOCVR

            self.__message(mitem)


    def __operate(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service threads.
        """

        from ...clients import IRCClient

        assert self.thread

        thread = self.thread
        member = thread.member
        cqueue = member.cqueue
        params = self.params

        clients = (
            thread.service
            .clients.childs
            .values())

        names = params.clients

        failure: set[bool] = set()


        for client in clients:

            name = client.name

            # Ignore unrelated clients
            if name not in names:
                continue

            assert isinstance(
                client, IRCClient)

            connected = (
                client.client
                .connected)

            # Bypass when disconnected
            if connected is False:
                failure.add(True)
                return None


            should = (
                client.params
                .client.nickname)

            current = (
                client.client
                .nickname)

            if current == should:
                return None


            failure.add(True)

            rawcmd = f'NICK :{should}'

            client.put_command(
                cqueue, rawcmd)


        self.__status(
            'failure'
            if any(failure)
            else 'normal')


    def __message(  # noqa: CFQ004
        self,
        mitem: 'IRCMessage',
    ) -> None:
        """
        Process the provided message item from the Robie thread.

        :param mitem: Item containing information for operation.
        """

        from ...clients import IRCClient

        robie = self.robie
        nickserv = self.__nickserv
        childs = robie.childs

        event = mitem.event
        command = event.command

        client = (
            childs.clients
            [mitem.client])

        assert isinstance(
            client, IRCClient)


        name = client.name

        if name not in nickserv:
            return NCNone

        service = (
            nickserv[name]
            .service)


        def _requested() -> bool:

            # Ignore when not NickServ
            if command != 'NOTICE':
                return False

            assert event.prefix
            assert event.params

            author = (
                event.prefix
                .split('!', 1)[0])

            message = (
                event.params
                .split(SPACED, 1)[1]
                .lstrip(':'))

            match = re_match(
                _IDENTIFY, message)

            # Ignore when not NickServ
            if author != service:
                return NCFalse

            return match is not None


        if (_requested()
                or command == '376'):
            self.__identify(client)


    def __identify(
        self,
        client: 'IRCClient',
    ) -> None:
        """
        Identify with the network nick services using password.

        :param client: Class instance for connecting to service.
        """

        assert self.thread

        thread = self.thread
        nickserv = self.__nickserv
        member = thread.member
        cqueue = member.cqueue

        name = client.name

        if name not in nickserv:
            return NCNone

        service = (
            nickserv[name]
            .service)

        password = (
            nickserv[name]
            .password)

        rawcmd = (
            f'PRIVMSG {service} '
            f':identify {password}')

        client.put_command(
            cqueue, rawcmd)



    def __status(
        self,
        status: StatusPluginStates,
    ) -> None:
        """
        Update or insert the status of the Robie child instance.

        :param status: One of several possible value for status.
        """

        thread = self.thread
        params = self.params

        if thread is None:
            return None

        plugins = (
            thread.service
            .plugins.childs)

        if 'status' not in plugins:
            return NCNone

        plugin = plugins['status']

        assert isinstance(
            plugin, StatusPlugin)

        (plugin.update(
            unique=self.name,
            group='Management',
            title='IRC',
            icon=params.status,
            state=status))
