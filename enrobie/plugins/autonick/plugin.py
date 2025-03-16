"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Type

from encommon.times import Timer
from encommon.types import NCNone

from .params import AutoNickPluginParams
from ..status import StatusPlugin
from ..status import StatusPluginStates
from ...robie.childs import RobiePlugin



class AutoNickPlugin(RobiePlugin):
    """
    Integrate with the Robie routine and perform operations.

    .. note::
       This plugin maintains configured nickname on server.
    """

    __started: bool

    __timer: Timer


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__started = False

        params = self.params

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

        assert self.thread

        thread = self.thread
        mqueue = thread.mqueue
        timer = self.__timer


        if not self.__started:
            self.__started = True
            self.__status('normal')


        if timer.ready():
            self.__operate()


        while not mqueue.empty:
            mqueue.get()


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
