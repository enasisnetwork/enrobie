"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Time

from .common import StatusPluginItem
from .common import StatusPluginStates
from .helpers import composedsc
from .helpers import composeirc
from .helpers import composemtm
from .params import StatusPluginIconParams
from .params import StatusPluginParams
from ...robie.childs import RobiePlugin

if TYPE_CHECKING:
    from ...robie.threads import RobieThread



class StatusPlugin(RobiePlugin):
    """
    Integrate with the Robie routine and perform operations.

    .. note::
       This plugin responds to inquiries about Robie status.
    """

    __status: dict[str, StatusPluginItem]


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__status = {}


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        # Nothing to do for plugin


    def operate(
        self,
        thread: 'RobieThread',
    ) -> None:
        """
        Perform the operation related to Homie service threads.

        :param thread: Child class instance for Chatting Robie.
        """

        robie = thread.robie
        mqueue = thread.mqueue
        member = thread.member
        cqueue = member.cqueue
        params = self.params
        status = self.__status

        assert isinstance(
            params, StatusPluginParams)

        command = params.command
        match: Optional[str]

        kinds = ['privmsg', 'chanmsg']


        while not mqueue.empty:

            mitem = mqueue.get()

            time = mitem.time
            kind = mitem.kind
            isme = mitem.isme
            family = mitem.family

            if kind not in kinds:
                continue

            if isme is True:
                continue

            if time.since > 15:
                continue  # NOCVR

            event = getattr(
                mitem, 'event')


            match = None

            if family == 'discord':
                match = command.dsc

            if family == 'irc':
                match = command.irc

            if family == 'mattermost':
                match = command.mtm

            if match is None:
                continue  # NOCVR


            message = event.message

            if message != match:
                continue  # NOCVR


            if family == 'discord':
                composedsc(
                    robie, cqueue,
                    mitem, status)

            if family == 'irc':
                composeirc(
                    robie, cqueue,
                    mitem, status)

            if family == 'mattermost':
                composemtm(
                    robie, cqueue,
                    mitem, status)


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

        robie.logger.log_i(
            base=self,
            name=self,
            item='status',
            unique=unique,
            state=state)

        object = StatusPluginItem(
            unique=unique,
            time=Time(),
            group=group,
            title=title,
            icon=icon,
            state=state)

        status[unique] = object
