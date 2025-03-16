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
    from ...robie.models import RobieMessage



class LoggerPlugin(RobiePlugin):
    """
    Integrate with the Robie routine and perform operations.

    .. note::
       This plugin allows for interacting with an LLM model.
    """

    __started: bool

    __history: LoggerHistory


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__started = False

        self.__history = (
            LoggerHistory(self))

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
    ) -> None:
        """
        Perform the operation related to Robie service threads.
        """

        assert self.thread

        thread = self.thread
        mqueue = thread.mqueue
        params = self.params
        history = self.history

        clients = (
            thread.service
            .clients.childs)

        names = params.clients
        output = params.output


        if not self.__started:
            self.__started = True
            self.__status('normal')


        kinds = ['privmsg', 'chanmsg']

        while not mqueue.empty:

            mitem = mqueue.get()

            name = mitem.client
            kind = mitem.kind

            # Ignore unrelated clients
            if name not in names:
                continue  # NOCVR

            # Ignore unrelated events
            if kind not in kinds:
                continue

            # Ignore disabled clients
            if name not in clients:
                continue  # NOCVR


            history.process(mitem)

            self.__status('normal')


            if output is not None:
                self.__writeout(mitem)


    def __writeout(
        self,
        mitem: 'RobieMessage',
    ) -> None:
        """
        Write the event out to the designated output file path.

        :param mitem: Item containing information for operation.
        """

        robie = self.robie
        childs = robie.childs
        persons = childs.persons
        clients = childs.clients
        params = self.params

        output = params.output

        _client = mitem.client
        _person = mitem.person
        author = mitem.author
        anchor = mitem.anchor
        message = mitem.message

        person = (
            persons[_person]
            if _person is not None
            else None)

        client = clients[_client]

        assert output is not None
        assert author is not None
        assert anchor is not None
        assert message is not None


        try:

            append = {
                'time': str(mitem.time),
                'client': client.name,
                'person': (
                    person.name
                    if person is not None
                    else None),
                'author': author,
                'anchor': anchor,
                'message': message}

            append_text(
                output,
                f'{dumps(append)}\n')

            self.__status('normal')

        except Exception as reason:

            self.__status('failure')

            robie.logger.log_e(
                base=self,
                name=self,
                item='writeout',
                status='exception',
                exc_info=reason)



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
            title='Logger',
            icon=params.status,
            state=status))
