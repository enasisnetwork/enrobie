"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread
from time import sleep as block_sleep
from typing import Any
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from enconnect.mattermost import Client
from enconnect.mattermost import ClientEvent
from enconnect.utils.http import _METHODS
from enconnect.utils.http import _PAYLOAD

from .command import MTMCommand
from .message import MTMMessage
from .params import MTMClientParams
from ...robie.addons import RobieQueue
from ...robie.childs import RobieClient

if TYPE_CHECKING:
    from ...robie.models import RobieCommand
    from ...robie.models import RobieMessage
    from ...robie.threads import RobieThread



class MTMClient(RobieClient):
    """
    Establish and maintain connection with the chat service.

    :param robie: Primary class instance for Chatting Robie.
    """


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """


    @property
    def family(
        self,
    ) -> Literal['mattermost']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'mattermost'


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


        def _put_mqueue() -> None:

            event = source.get()

            self.put_message(
                target, event)


        def _get_cqueue() -> None:

            citem = cqueue.get()

            assert isinstance(
                citem, MTMCommand)

            client.request(
                method=citem.method,
                path=citem.path,
                params=citem.params,
                json=citem.json,
                timeout=10)


        def _continue() -> bool:

            return (
                not vacate.is_set()
                and daerht.is_alive())


        def _debug_logger(
            **kwargs: Any,
        ) -> None:

            assert not any([
                kwargs.get('level'),
                kwargs.get('base'),
                kwargs.get('name')])

            robie.logger.log_d(
                base=self,
                name=self,
                **kwargs)


        client = Client(
            params.client,
            _debug_logger)

        source = client.mqueue


        def _operate() -> None:

            try:
                client.operate()

            except ConnectionError:
                return None

            except Exception as reason:

                robie.logger.log_e(
                    base=self,
                    name=self,
                    status='exception',
                    exc_info=reason)

                return None


        def _routine() -> None:

            while _continue():

                robie.logger.log_i(
                    base=self,
                    name=self,
                    status='connect')

                _operate()

                robie.logger.log_i(
                    base=self,
                    name=self,
                    status='severed')

                block_sleep(1)


        daerht = Thread(
            target=_routine)

        daerht.start()


        while _continue():

            if not cqueue.empty:
                _get_cqueue()

            while not source.empty():
                _put_mqueue()

            block_sleep(0.05)


        client.stop()

        while daerht.is_alive():
            daerht.join(1)

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
