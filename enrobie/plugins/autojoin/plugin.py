"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from time import sleep as block_sleep
from typing import TYPE_CHECKING
from typing import Type

from encommon.times import Timer
from encommon.types import NCNone
from encommon.types.strings import SPACED

from .params import AutoJoinPluginParams
from ..status import StatusPlugin
from ..status import StatusPluginStates
from ...robie.childs import RobiePlugin

if TYPE_CHECKING:
    from ...clients.irc.message import IRCMessage



_CHANNELS = dict[str, set[str]]



class AutoJoinPlugin(RobiePlugin):
    """
    Integrate with the Robie routine and perform operations.

    .. note::
       This plugin maintains joined for configured channels.
    """

    __started: bool

    __should: _CHANNELS
    __joined: _CHANNELS

    __timer: Timer


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__started = False

        params = self.params


        should: _CHANNELS = {}
        joined: _CHANNELS = {}

        channels = params.channels

        for channel in channels:

            name = channel.client

            if name not in should:
                should[name] = set()
                joined[name] = set()

            should[name].add(
                channel.channel)

        self.__should = should
        self.__joined = joined


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
    ) -> Type[AutoJoinPluginParams]:
        """
        Return the configuration parameters relevant for class.

        :returns: Configuration parameters relevant for class.
        """

        return AutoJoinPluginParams


    @property
    def params(
        self,
    ) -> AutoJoinPluginParams:
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        params = super().params

        assert isinstance(
            params,
            AutoJoinPluginParams)

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
        should = self.__should
        joined = self.__joined
        member = thread.member
        cqueue = member.cqueue

        clients = (
            thread.service
            .clients.childs)

        failure: set[bool] = set()


        for name in should:

            # Ignore disabled clients
            if name not in clients:
                return NCNone

            client = clients[name]

            assert isinstance(
                client, IRCClient)

            connected = (
                client.client
                .connected)

            # Bypass when disconnected
            if connected is False:
                failure.add(True)
                return None

            _should = should[name]
            _joined = joined[name]

            for join in _should:

                if join in _joined:
                    continue  # NOCVR

                failure.add(True)

                rawcmd = f'JOIN :{join}'

                client.put_command(
                    cqueue, rawcmd)


        self.__status(
            'failure'
            if any(failure)
            else 'normal')


    def __message(
        self,
        mitem: 'IRCMessage',
    ) -> None:
        """
        Process the provided message item from the Robie thread.

        :param mitem: Item containing information for operation.
        """

        from ...clients import IRCClient

        robie = self.robie
        childs = robie.childs
        clients = childs.clients
        joined = self.__joined

        _client = mitem.client
        isme = mitem.isme
        event = mitem.event

        client = clients[_client]

        if _client not in joined:
            return NCNone

        assert isinstance(
            client, IRCClient)

        _joined = joined[_client]


        command = event.command
        params = event.params

        if params is None:
            return NCNone

        split = params.split(SPACED)

        current = (
            client.client
            .nickname)


        if command == '376':

            _joined.clear()

            # Allow for identify
            block_sleep(5)

            self.__operate()


        elif (command == 'JOIN'
                and isme is True):

            channel = split[0][1:]

            _joined.add(channel)


        elif command == 'KICK':

            channel = split[0]
            target = split[1]

            if target == current:
                _joined.remove(channel)


        elif (command == 'PART'
                and isme is True):

            channel = split[0]

            _joined.remove(channel)


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
