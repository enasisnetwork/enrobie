"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING
from typing import Type

from encommon.times import Timer
from encommon.types import NCNone

from enconnect.irc import ClientEvent

from .params import AutoJoinPluginParams
from ..status import StatusPlugin
from ..status import StatusPluginStates
from ...robie.childs import RobiePlugin

if TYPE_CHECKING:
    from ...clients import IRCClient
    from ...robie.threads import RobieThread



_CHANNELS = dict[str, set[str]]



class AutoJoinPlugin(RobiePlugin):
    """
    Integrate with the Robie routine and perform operations.

    .. note::
       This plugin maintains joined for configured channels.
    """

    __should: _CHANNELS
    __joined: _CHANNELS

    __timer: Timer


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        params = self.params

        channels = params.channels

        self.__joined = {}


        should: _CHANNELS = {}
        joined: _CHANNELS = {}

        for channel in channels:

            name = channel.client

            if name not in should:
                should[name] = set()
                joined[name] = set()

            should[name].add(
                channel.channel)

        self.__should = should
        self.__joined = joined


        self.__timer = Timer(5)

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
        thread: 'RobieThread',
    ) -> None:
        """
        Perform the operation related to Homie service threads.

        :param thread: Child class instance for Chatting Robie.
        """

        from ...clients import IRCClient

        should = self.__should
        joined = self.__joined
        robie = self.robie
        childs = robie.childs
        clients = childs.clients
        mqueue = thread.mqueue
        member = thread.member
        cqueue = member.cqueue
        timer = self.__timer


        if timer.ready():
            self.__operate(thread)


        def _autojoin() -> None:

            joined[name] = set()

            assert isinstance(
                client, IRCClient)

            _should = should[name]
            _joined = joined[name]

            for join in _should:

                if join in _joined:
                    continue  # NOCVR

                rawcmd = f'JOIN :{join}'

                client.put_command(
                    cqueue, rawcmd)


        while not mqueue.empty:

            mitem = mqueue.get()

            name = mitem.client
            family = mitem.family

            if family != 'irc':
                continue  # NOCVR

            client = clients[name]

            assert isinstance(
                client, IRCClient)

            event = getattr(
                mitem, 'event')

            assert isinstance(
                event, ClientEvent)

            self.__process(
                client, event)

            if event.command == '376':
                _autojoin()


    def __operate(
        self,
        thread: 'RobieThread',
    ) -> None:
        """
        Perform the operation related to Homie service threads.

        :param thread: Child class instance for Chatting Robie.
        """

        from ...clients import IRCClient

        should = self.__should
        joined = self.__joined
        robie = self.robie
        childs = robie.childs
        clients = childs.clients
        member = thread.member
        cqueue = member.cqueue

        failure: set[bool] = set()


        def _autojoin() -> None:

            if name not in clients:
                return NCNone

            client = clients[name]

            assert isinstance(
                client, IRCClient)

            connected = (
                client.client
                .connected)

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


        for name in should:
            _autojoin()


        self.__status(
            'failure'
            if any(failure)
            else 'normal')


    def __process(
        self,
        client: 'IRCClient',
        event: ClientEvent,
    ) -> None:
        """
        Process the provided message item from the Robie thread.

        :param client: Client class instance for Chatting Robie.
        :param event: Raw event received from the network peer.
        """

        joined = self.__joined
        name = client.name

        if name not in joined:
            return NCNone

        _joined = joined[name]


        isme = event.isme
        command = event.command
        params = event.params

        if params is None:
            return NCNone

        split = params.split(' ')

        current = (
            client.client
            .nickname)


        if (command == 'JOIN'
                and isme is True):

            channel = split[0][1:]

            _joined.add(channel)


        if command == 'KICK':

            channel = split[0]
            target = split[1]

            if target == current:
                _joined.remove(channel)


        if (command == 'PART'
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

        robie = self.robie
        childs = robie.childs
        plugins = childs.plugins
        params = self.params

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
