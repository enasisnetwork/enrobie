"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional
from typing import Type
from typing import Union

from encommon.types import NCNone

from .current import NagiosCurrent
from .helpers import composedsc
from .helpers import composeirc
from .helpers import composemtm
from .params import NagiosPluginParams
from ..ainswer import AinswerTool
from ..status import StatusPlugin
from ..status import StatusPluginStates
from ...robie.childs import RobiePerson
from ...robie.childs import RobiePlugin
from ...robie.models import RobieMessage



class NagiosPlugin(RobiePlugin):
    """
    Integrate with the Robie routine and perform operations.

    .. note::
       This plugin allows for connecting to Nagios Console.
    """

    __started: bool

    __current: NagiosCurrent


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__started = False

        self.__current = (
            NagiosCurrent(self))

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
    ) -> Type[NagiosPluginParams]:
        """
        Return the configuration parameters relevant for class.

        :returns: Configuration parameters relevant for class.
        """

        return NagiosPluginParams


    @property
    def params(
        self,
    ) -> NagiosPluginParams:
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        params = super().params

        assert isinstance(
            params,
            NagiosPluginParams)

        return params


    @property
    def current(
        self,
    ) -> NagiosCurrent:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__current


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service threads.

        :param thread: Child class instance for Chatting Robie.
        """

        assert self.thread

        thread = self.thread
        mqueue = thread.mqueue
        params = self.params

        command = params.command

        names = (
            self.params.clients)


        match: Optional[str]

        kinds = ['privmsg', 'chanmsg']


        if not self.__started:
            self.__started = True
            self.__status('normal')


        while not mqueue.empty:

            mitem = mqueue.get()

            name = mitem.client
            time = mitem.time
            kind = mitem.kind
            family = mitem.family
            isme = mitem.isme
            message = mitem.message

            # Ignore unrelated events
            if kind not in kinds:
                continue

            # Ignore unrelated clients
            if name not in names:
                continue  # NOCVR

            # Ignore event from client
            if isme is True:
                continue

            # Ignore expired messages
            if time.since > 15:
                continue  # NOCVR

            # Basic trust enforcement
            if self.notrust(mitem):
                continue


            match = None

            if family == 'discord':
                match = command.dsc

            if family == 'irc':
                match = command.irc

            if family == 'mattermost':
                match = command.mtm

            # Ignore unrelated clients
            if match is None:
                continue  # NOCVR

            # Ignore unrelated message
            if message != match:
                continue


            if family == 'discord':
                composedsc(self, mitem)

            if family == 'irc':
                composeirc(self, mitem)

            if family == 'mattermost':
                composemtm(self, mitem)


    def trusted(
        self,
        check: Union[str, RobiePerson, RobieMessage],
    ) -> bool:
        """
        Return the boolean indicating whether person is trusted.

        :param check: Validate the person is trusted by plugin.
        :returns: Boolean indicating whether person is trusted.
        """

        params = self.params
        trusted = params.trusted

        if trusted is None:
            return True

        if isinstance(check, RobieMessage):

            if not check.person:
                return False

            check = check.person

        elif isinstance(check, RobiePerson):
            check = check.name

        return check in trusted


    def notrust(
        self,
        check: Union[str, RobiePerson, RobieMessage],
    ) -> bool:
        """
        Return the boolean indicating whether person is trusted.

        :param check: Validate the person is trusted by plugin.
        :returns: Boolean indicating whether person is trusted.
        """

        return not self.trusted(check)


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
            group='Extensions',
            title='Nagios Monitor',
            icon=params.status,
            state=status))


    def ainswer(
        self,
    ) -> list[AinswerTool]:
        """
        Return the Ainswer tools that are related to the plugin.

        :returns: Ainswer tools that are related to the plugin.
        """

        from .ainswer import nagios_current

        return [nagios_current]
