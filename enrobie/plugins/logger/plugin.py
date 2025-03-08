"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import dumps
from typing import TYPE_CHECKING
from typing import Type

from encommon.types import NCNone
from encommon.utils import append_text

from .history import LoggerHistory
from .params import LoggerPluginParams
from ..status import StatusPlugin
from ..status import StatusPluginStates
from ...robie.childs import RobiePlugin

if TYPE_CHECKING:
    from ...robie.threads import RobieThread



class LoggerPlugin(RobiePlugin):
    """
    Integrate with the Robie routine and perform operations.

    .. note::
       This plugin allows for interacting with an LLM model.
    """

    __history: LoggerHistory


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__history = (
            LoggerHistory(self))

        self.__status('normal')


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
    ) -> Type[LoggerPluginParams]:
        """
        Return the configuration parameters relevant for class.

        :returns: Configuration parameters relevant for class.
        """

        return LoggerPluginParams


    @property
    def params(
        self,
    ) -> LoggerPluginParams:
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        params = super().params

        assert isinstance(
            params,
            LoggerPluginParams)

        return params


    @property
    def history(
        self,
    ) -> LoggerHistory:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__history


    def operate(
        self,
        thread: 'RobieThread',
    ) -> None:
        """
        Perform the operation related to Homie service threads.

        :param thread: Child class instance for Chatting Robie.
        """

        robie = self.robie
        childs = robie.childs
        clients = childs.clients
        mqueue = thread.mqueue
        history = self.history

        names = (
            self.params.clients)

        output = (
            self.params.output)


        kinds = ['privmsg', 'chanmsg']

        while not mqueue.empty:

            mitem = mqueue.get()

            name = mitem.client
            kind = mitem.kind
            author = mitem.author
            anchor = mitem.anchor
            message = mitem.message

            if name not in names:
                continue  # NOCVR

            if kind not in kinds:
                continue

            assert author is not None
            assert anchor is not None
            assert message is not None

            client = clients[name]

            history.insert(
                client, author[0],
                anchor, message)


            if output is None:
                continue  # NOCVR

            append = {
                'client': client.name,
                'time': str(mitem.time),
                'author': author,
                'anchor': anchor,
                'message': message}

            append_text(
                output,
                f'{dumps(append)}\n')


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
            group='Extensions',
            title='Logger',
            icon=params.status,
            state=status))
