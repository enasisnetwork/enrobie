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

from encommon.types import NCNone

from enconnect.mattermost import Client
from enconnect.mattermost import ClientEvent
from enconnect.utils.http import _METHODS
from enconnect.utils.http import _PAYLOAD

from .command import MTMCommand
from .message import MTMMessage
from .params import MTMClientParams
from ...plugins import StatusPlugin
from ...plugins import StatusPluginStates
from ...robie.addons import RobieQueue
from ...robie.childs import RobieClient
from ...utils import DupliThread

if TYPE_CHECKING:
    from ...robie.models import RobieCommand
    from ...robie.models import RobieMessage
    from ...robie.threads import RobieThread



class MTMClient(RobieClient):
    """
    Establish and maintain connection with the chat service.
    """

    __client: Client


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        params = self.params

        assert isinstance(
            params, MTMClientParams)

        client = Client(
            params.client,
            self.__debugger)

        self.__client = client


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        # Nothing to do for client


    @property
    def family(
        self,
    ) -> Literal['mattermost']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'mattermost'


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
        thread: 'RobieThread',
    ) -> None:
        """
        Perform the operation related to Homie service threads.

        :param thread: Child class instance for Chatting Robie.
        """

        robie = thread.robie
        member = thread.member
        target = member.mqueue
        cqueue = thread.cqueue
        vacate = member.vacate
        params = self.params

        assert isinstance(
            params, MTMClientParams)

        delay = params.delay

        self.__status('pending')


        def _put_mqueue() -> None:

            event = source.get()

            self.put_message(
                target, event)


        def _get_cqueue() -> None:

            citem = cqueue.get()

            assert isinstance(
                citem, MTMCommand)

            try:
                client.request(
                    method=citem.method,
                    path=citem.path,
                    params=citem.params,
                    json=citem.json,
                    timeout=10)

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


    def get_message(
        self,
        event: Optional[ClientEvent] = None,
    ) -> MTMMessage:
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

        return MTMMessage(self, event)


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


    def get_command(
        self,
        method: Optional[_METHODS] = None,
        path: Optional[str] = None,
        params: Optional[_PAYLOAD] = None,
        json: Optional[_PAYLOAD] = None,
    ) -> MTMCommand:
        """
        Return the new item containing information for operation.

        .. note::
           Though parameters are marked optional, that is not
           necessarily the case; for typing purposes one cannot
           introduce required parameters outside of the parent.

        :returns: New item containing information for operation.
        :param method: Method for operation with the API server.
        :param path: Path for the location to upstream endpoint.
        :param params: Optional parameters included in request.
        :param json: Optional JSON payload included in request.
        """

        assert method is not None
        assert path is not None

        return MTMCommand(
            self,
            method, path,
            params, json)


    def put_command(
        self,
        cqueue: RobieQueue['RobieCommand'],
        method: Optional[_METHODS] = None,
        path: Optional[str] = None,
        params: Optional[_PAYLOAD] = None,
        json: Optional[_PAYLOAD] = None,
    ) -> None:
        """
        Insert the new item containing information for operation.

        .. note::
           Though parameters are marked optional, that is not
           necessarily the case; for typing purposes one cannot
           introduce required parameters outside of the parent.

        :param cqueue: Queue instance where the item is received.
        :param method: Method for operation with the API server.
        :param path: Path for the location to upstream endpoint.
        :param params: Optional parameters included in request.
        :param json: Optional JSON payload included in request.
        """

        citem = (
            self.get_command(
                method, path,
                params, json))

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

        payload = {
            'channel_id': target,
            'message': content}

        return (
            self.get_command(
                'post', 'posts',
                json=payload))


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

        robie = self.robie
        childs = robie.childs
        plugins = childs.plugins
        params = self.params

        assert isinstance(
            params, MTMClientParams)

        if 'status' not in plugins:
            return NCNone

        plugin = plugins['status']

        assert isinstance(
            plugin, StatusPlugin)

        (plugin.update(
            unique=self.name,
            group='Connections',
            title='Mattermost',
            icon=params.status,
            state=status))
