"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional
from typing import TYPE_CHECKING
from typing import Type
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
from ...robie.childs import RobiePlugin

if TYPE_CHECKING:
    from ...robie.threads import RobieThread



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


    def operate(
        self,
        thread: 'RobieThread',
    ) -> None:
        """
        Perform the operation related to Homie service threads.

        :param thread: Child class instance for Chatting Robie.
        """

        mqueue = thread.mqueue
        member = thread.member
        cqueue = member.cqueue
        params = self.params
        status = self.__status

        command = params.command
        match: Optional[str]

        kinds = ['privmsg', 'chanmsg']


        self.report(thread)


        while not mqueue.empty:

            mitem = mqueue.get()

            time = mitem.time
            kind = mitem.kind
            family = mitem.family
            isme = mitem.isme
            message = mitem.message

            if kind not in kinds:
                continue

            if isme is True:
                continue

            if time.since > 15:
                continue  # NOCVR


            match = None

            if family == 'discord':
                match = command.dsc

            if family == 'irc':
                match = command.irc

            if family == 'mattermost':
                match = command.mtm

            if match is None:
                continue  # NOCVR

            if message != match:
                continue  # NOCVR


            if family == 'discord':
                composedsc(
                    self, cqueue,
                    mitem, status)

            if family == 'irc':
                composeirc(
                    self, cqueue,
                    mitem, status)

            if family == 'mattermost':
                composemtm(
                    self, cqueue,
                    mitem, status)


    def report(
        self,
        thread: 'RobieThread',
    ) -> None:
        """
        Perform the operation related to Homie service threads.

        :param thread: Child class instance for Chatting Robie.
        """

        status = self.__status
        stated = self.__stated
        robie = self.robie
        params = self.params
        childs = robie.childs
        clients = childs.clients
        member = thread.member
        cqueue = member.cqueue

        if not params.reports:
            return NCNone


        def _send_report() -> None:

            if family == 'discord':
                reportdsc(
                    self, client,
                    cqueue,
                    _status, report)

            if family == 'irc':
                reportirc(
                    self, client,
                    cqueue,
                    _status, report)

            if family == 'mattermost':
                reportmtm(
                    self, client,
                    cqueue,
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
                return None

        robie.logger.log_i(
            base=self,
            name=self,
            item='status',
            unique=unique,
            state=state)

        status[unique] = object
