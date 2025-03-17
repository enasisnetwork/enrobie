"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional
from typing import TYPE_CHECKING
from typing import Type
from typing import Union
from typing import get_args

from encommon.times import Time
from encommon.types import NCNone

from .common import StatusPluginItem
from .common import StatusPluginStates
from .helpers import composedsc
from .helpers import composeirc
from .helpers import composemtm
from .helpers import reportdsc
from .helpers import reportirc
from .helpers import reportmtm
from .params import StatusPluginIconParams
from .params import StatusPluginParams
from ...robie.childs import RobiePerson
from ...robie.childs import RobiePlugin
from ...robie.models import RobieMessage

if TYPE_CHECKING:
    from .common import StatusPluginItems



_STATES = list(
    get_args(StatusPluginStates))



class StatusPlugin(RobiePlugin):
    """
    Integrate with the Robie routine and perform operations.

    .. note::
       This plugin responds to inquiries about Robie status.
    """

    __status: dict[str, StatusPluginItem]
    __stated: dict[str, dict[str, str]]


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__status = {}
        self.__stated = {}


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        # Nothing to do for plugin


    @classmethod
    def schema(
        cls,
    ) -> Type[StatusPluginParams]:
        """
        Return the configuration parameters relevant for class.

        :returns: Configuration parameters relevant for class.
        """

        return StatusPluginParams


    @property
    def params(
        self,
    ) -> StatusPluginParams:
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        params = super().params

        assert isinstance(
            params,
            StatusPluginParams)

        return params


    @property
    def status(
        self,
    ) -> 'StatusPluginItems':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return dict(self.__status)


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service threads.
        """

        assert self.thread

        thread = self.thread
        mqueue = thread.mqueue
        params = self.params

        command = params.command


        match: Optional[str]

        kinds = ['privmsg', 'chanmsg']


        self.report()


        while not mqueue.empty:

            mitem = mqueue.get()

            time = mitem.time
            kind = mitem.kind
            family = mitem.family
            isme = mitem.isme
            message = mitem.message

            # Ignore unrelated events
            if kind not in kinds:
                continue

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


    def report(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service threads.
        """

        assert self.thread

        thread = self.thread
        status = self.__status
        stated = self.__stated
        params = self.params

        clients = (
            thread.service
            .clients.childs)

        if not params.reports:
            return NCNone


        def _send_report() -> None:

            if family == 'discord':
                reportdsc(
                    self, client,
                    _status, report)

            if family == 'irc':
                reportirc(
                    self, client,
                    _status, report)

            if family == 'mattermost':
                reportmtm(
                    self, client,
                    _status, report)


        reports = params.reports


        for report in reports:

            name = report.client
            target = report.target
            delay = report.delay
            states = (
                report.states
                or _STATES)

            unique = (
                f'{name}/{target}')

            # Ignore disabled clients
            if name not in clients:
                continue  # NOCVR

            client = clients[name]

            family = client.family

            if unique not in stated:
                stated[unique] = {}

            _stated = stated[unique]


            items = status.items()

            for _unique, _status in items:

                time = _status.time
                since = time.since

                if since < delay:
                    continue  # NOCVR

                state = _status.state

                _state = (
                    _stated.get(_unique))

                if state == _state:
                    continue

                _stated[_unique] = state


                if state not in states:
                    continue  # NOCVR

                _send_report()


    def update(
        self,
        unique: str,
        group: str,
        title: str,
        icon: StatusPluginIconParams,
        state: StatusPluginStates,
    ) -> None:
        """
        Update or insert the status of the Robie child instance.

        :param unique: Unique identifier to use for the status.
        :param group: Name for the group the status is membered.
        :param title: Friendly name of the related unique entry.
        :param icon: Optional icon object if supported platform.
        :param state: One of several possible value for status.
        """

        robie = self.robie
        status = self.__status

        object = StatusPluginItem(
            unique=unique,
            time=Time(),
            group=group,
            title=title,
            icon=icon,
            state=state)

        if unique in status:

            _object = status[unique]
            _state = _object.state

            if state == _state:
                return NCNone

        robie.logger.log_i(
            base=self,
            name=self,
            item='status',
            unique=unique,
            state=state)

        status[unique] = object


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
