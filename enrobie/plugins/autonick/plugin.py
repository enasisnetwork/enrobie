"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.times import Timer

from .params import AutoNickPluginParams
from ..status import StatusPlugin
from ..status import StatusPluginStates
from ...robie.childs import RobiePlugin

if TYPE_CHECKING:
    from ...robie.threads import RobieThread



class AutoNickPlugin(RobiePlugin):
    """
    Integrate with the Robie routine and perform operations.

    .. note::
       This plugin maintains configured nickname on server.
    """

    __timer: Timer


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__timer = Timer(5)

        self.__status('pending')


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """


    def operate(
        self,
        thread: 'RobieThread',
    ) -> None:
        """
        Perform the operation related to Homie service threads.

        :param thread: Child class instance for Chatting Robie.
        """

        mqueue = thread.mqueue
        timer = self.__timer


        if timer.ready():
            self.__operate(thread)


        while not mqueue.empty:
            mqueue.get()


    def __operate(
        self,
        thread: 'RobieThread',
    ) -> None:
        """
        Perform the operation related to Homie service threads.

        :param thread: Child class instance for Chatting Robie.
        """

        from ...clients import IRCClient
        from ...clients import IRCClientParams

        robie = self.robie
        childs = robie.childs
        member = thread.member
        cqueue = member.cqueue
        params = self.params

        clients = (
            childs.clients
            .values())

        assert isinstance(
            params,
            AutoNickPluginParams)

        names = params.clients

        failure: set[bool] = set()


        def _autonick() -> None:

            assert isinstance(
                client, IRCClient)

            connected = (
                client.client
                .connected)

            if connected is False:
                failure.add(True)
                return None

            params = client.params

            assert isinstance(
                params,
                IRCClientParams)

            should = (
                params.client
                .nickname)

            current = (
                client.client
                .nickname)

            if current == should:
                return None

            failure.add(True)

            rawcmd = f'NICK :{should}'

            client.put_command(
                cqueue, rawcmd)


        for client in clients:

            name = client.name
            family = client.family

            if family != 'irc':
                continue

            if name in names:
                _autonick()


        self.__status(
            'failure'
            if any(failure)
            else 'normal')



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

        assert isinstance(
            params,
            AutoNickPluginParams)

        if 'status' not in plugins:
            return None

        plugin = plugins['status']

        assert isinstance(
            plugin, StatusPlugin)

        (plugin.update(
            unique=self.name,
            group='Management',
            title='IRC',
            icon=params.status,
            state=status))
