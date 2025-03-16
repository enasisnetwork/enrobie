"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Event
from threading import Thread
from threading import enumerate as thread_enumerate
from time import sleep as block_sleep
from typing import Any
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING
from typing import Type

from encommon.types import NCNone
from encommon.types.strings import SPACED

from enconnect.irc import Client
from enconnect.irc import ClientEvent

from .command import IRCCommand
from .message import IRCMessage
from .params import IRCClientParams
from .states import ClientChannels
from ...plugins import StatusPlugin
from ...plugins import StatusPluginStates
from ...robie.addons import RobieQueue
from ...robie.childs import RobieClient
from ...utils import ClientPublish
from ...utils import DupliThread

if TYPE_CHECKING:
    from ...robie.models import RobieCommand
    from ...robie.models import RobieMessage



class IRCClient(RobieClient):
    """
    Establish and maintain connection with the chat service.
    """

    __client: Client
    __channels: ClientChannels
    __publish: ClientPublish


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        params = self.params

        client = Client(
            params.client,
            self.__debugger)

        self.__client = client

        self.__channels = (
            ClientChannels())

        self.__publish = (
            ClientPublish())


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        # Nothing to do for client


    @classmethod
    def schema(
        cls,
    ) -> Type[IRCClientParams]:
        """
        Return the configuration parameters relevant for class.

        :returns: Configuration parameters relevant for class.
        """

        return IRCClientParams


    @property
    def params(
        self,
    ) -> IRCClientParams:
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        params = super().params

        assert isinstance(
            params,
            IRCClientParams)

        return params


    @property
    def family(
        self,
    ) -> Literal['irc']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'irc'


    @property
    def channels(
        self,
    ) -> ClientChannels:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__channels


    @property
    def publish(
        self,
    ) -> ClientPublish:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__publish


    @property
    def client(
        self,
    ) -> Client:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__client


    def operate(  # noqa: CFQ001
        self,
    ) -> None:
        """
        Perform the operation related to Robie service threads.
        """

        assert self.thread

        thread = self.thread
        robie = thread.robie
        member = thread.member
        target = member.mqueue
        cqueue = thread.cqueue
        vacate = member.vacate
        params = self.params

        delay = params.delay

        self.__status('pending')


        def _put_mqueue() -> None:

            event = source.get()

            try:
                self.__event(event)


            except Exception as reason:

                robie.logger.log_e(
                    base=self,
                    name=self,
                    status='exception',
                    exc_info=reason)

            self.put_message(
                target, event)


        def _get_cqueue() -> None:

            if not client.connected:
                return NCNone

            citem = cqueue.get()

            assert isinstance(
                citem, IRCCommand)

            try:
                client.socket_send(
                    citem.event)

            except Exception as reason:

                robie.logger.log_e(
                    base=self,
                    name=self,
                    status='exception',
                    exc_info=reason)


        def _continue() -> bool:

            return (
                not vacate.is_set()
                and daerht.is_alive())


        client = self.__client
        source = client.mqueue


        def _operate() -> None:

            try:

                client.operate()

                self.__status('pending')

            except ConnectionError:
                self.__status('failure')

            except Exception as reason:

                robie.logger.log_e(
                    base=self,
                    name=self,
                    status='exception',
                    exc_info=reason)

                self.__status('failure')

            finally:
                pending.set()


        def _routine() -> None:

            while _continue():

                robie.logger.log_i(
                    base=self,
                    name=self,
                    status='connect')

                pending.set()

                _operate()

                robie.logger.log_i(
                    base=self,
                    name=self,
                    status='severed')

                block_sleep(delay)


        pending = Event()


        name = (
            f'{self.name}'
            '_thread_client')

        threads = (
            x.name for x in
            thread_enumerate())

        if name in threads:
            raise DupliThread(name)

        daerht = Thread(
            name=name,
            target=_routine)

        daerht.start()


        def _connected() -> bool:

            return all([
                client.connected,
                client.nickname])


        while _continue():

            if (pending.is_set()
                    and _connected()):

                self.__status('normal')

                pending.clear()

            if not cqueue.empty:
                _get_cqueue()

            block_sleep(0.025)

            while not source.empty():
                _put_mqueue()

            block_sleep(0.025)


        client.stop()

        while daerht.is_alive():
            daerht.join(1)

        daerht.join()

        while not source.empty():
            _put_mqueue()  # NOCVR


    def __event(  # noqa: CFQ001
        self,
        event: ClientEvent,
    ) -> None:
        """
        Process the provided message item from the Robie thread.

        :param event: Raw event received from the network peer.
        """

        command = event.command
        params = event.params
        prefix = event.prefix


        if command == '353':

            assert params

            chan, members = (
                params.split(SPACED, 3)[2:])

            assert members

            _names = [
                x.lstrip('~@%&+')
                for x in
                (members.lstrip(':')
                 .split(SPACED))]

            for name in _names:
                (self.channels
                 .add_member(chan, name))


        if command == 'JOIN':

            assert prefix
            assert params

            nick = prefix.split('!')[0]
            chan = (
                params.lstrip(':')
                .split(SPACED, 1)[0])

            if event.whome == nick:
                (self.channels
                 .clear_members(chan))

            (self.channels
             .add_member(chan, nick))


        if command == 'PART':

            assert prefix
            assert params

            nick = prefix.split('!')[0]
            chan = (
                params.lstrip(':')
                .split(SPACED, 1)[0])

            (self.channels
             .del_member(chan, nick))


        if command == 'KICK':

            assert params

            chan, nick, _ = (
                params.split(SPACED, 3))

            (self.channels
             .del_member(chan, nick))


        if command in ['332', 'TOPIC']:

            assert params

            topic: Optional[str] = None

            if command == '332':

                chan = (
                    params
                    .split(SPACED, 2)[1])

                topic = (
                    params
                    .split(SPACED, 2)[2]
                    .lstrip(':'))

            if command == 'TOPIC':

                chan = (
                    params
                    .split(SPACED, 1)[0])

                topic = (
                    params
                    .split(SPACED, 1)[1]
                    .lstrip(':'))

            assert topic is not None

            (self.channels
             .set_topic(chan, topic))


        if command == 'NICK':

            assert prefix
            assert params

            current = prefix.split('!')[0]
            update = params.lstrip(':')

            (self.channels
             .rename_member(current, update))


    def get_message(
        self,
        event: Optional[ClientEvent] = None,
    ) -> IRCMessage:
        """
        Return the new item containing information for operation.

        .. note::
           Though parameters are marked optional, that is not
           necessarily the case; for typing purposes one cannot
           introduce required parameters outside of the parent.

        :param event: Raw event received from the network peer.
        :returns: New item containing information for operation.
        """

        assert event is not None

        return IRCMessage(self, event)


    def put_message(
        self,
        mqueue: RobieQueue['RobieMessage'],
        event: Optional[ClientEvent] = None,
    ) -> None:
        """
        Insert the new item containing information for operation.

        .. note::
           Though parameters are marked optional, that is not
           necessarily the case; for typing purposes one cannot
           introduce required parameters outside of the parent.

        :param mqueue: Queue instance where the item is received.
        :param event: Raw event received from the network peer.
        """

        mitem = self.get_message(event)

        mqueue.put(mitem)

        self.__publish.publish(mitem)


    def get_command(
        self,
        event: Optional[str] = None,
    ) -> IRCCommand:
        """
        Return the new item containing information for operation.

        .. note::
           Though parameters are marked optional, that is not
           necessarily the case; for typing purposes one cannot
           introduce required parameters outside of the parent.

        :param event: Raw event to be sent to the network peer.
        :returns: New item containing information for operation.
        """

        assert event is not None

        return IRCCommand(self, event)


    def put_command(
        self,
        cqueue: RobieQueue['RobieCommand'],
        event: Optional[str] = None,
    ) -> None:
        """
        Insert the new item containing information for operation.

        .. note::
           Though parameters are marked optional, that is not
           necessarily the case; for typing purposes one cannot
           introduce required parameters outside of the parent.

        :param cqueue: Queue instance where the item is received.
        :param event: Raw event to be sent to the network peer.
        """

        citem = self.get_command(event)

        cqueue.put(citem)


    def compose(
        self,
        target: str,
        content: str,
    ) -> 'RobieCommand':
        """
        Compose the message and transmit using the chat client.

        .. note::
           Though parameters are marked optional, that is not
           necessarily the case; for typing purposes one cannot
           introduce required parameters outside of the parent.

        :param target: Where the composed message will be sent.
        :param content: Content that will be source of message.
        """

        assert target is not None

        return (
            self.get_command(
                f'PRIVMSG {target}'
                f' :{content}'))


    def __debugger(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided keyword arguments into logger object.

        :param kwargs: Keyword arguments for populating message.
        """

        robie = self.robie

        assert not any([
            kwargs.get('level'),
            kwargs.get('base'),
            kwargs.get('name')])

        robie.logger.log_d(
            base=self,
            name=self,
            **kwargs)


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
            return NCNone

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
            group='Connections',
            title='IRC',
            icon=params.status,
            state=status))
