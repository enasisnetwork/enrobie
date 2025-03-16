"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING
from typing import Type

from encommon.types import DictStrAny
from encommon.types import NCNone

from .child import RobieChild
from ..addons import RobieQueue
from ...utils import ClientChannels

if TYPE_CHECKING:
    from ..models import RobieCommand
    from ..models import RobieMessage
    from ..params import RobieClientParams
    from ..threads import RobieClientThread



class RobieClient(RobieChild):
    """
    Establish and maintain connection with the chat service.
    """

    __thread: Optional['RobieClientThread'] = None


    @property
    def family(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        raise NotImplementedError


    @property
    def kind(
        self,
    ) -> Literal['client']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'client'


    @property
    def channels(
        self,
    ) -> ClientChannels:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        raise NotImplementedError


    @classmethod
    def schema(
        cls,
    ) -> Type['RobieClientParams']:
        """
        Return the configuration parameters relevant for class.

        :returns: Configuration parameters relevant for class.
        """

        raise NotImplementedError


    @property
    def thread(
        self,
    ) -> Optional['RobieClientThread']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        from ..threads import (
            RobieClientThread)

        thread = self.__thread

        if thread is None:
            return NCNone

        assert isinstance(
            thread,
            RobieClientThread)

        return thread


    @thread.setter
    def thread(
        self,
        value: 'RobieClientThread',
    ) -> None:
        """
        Update the value for the attribute from class instance.
        """

        from ..threads import (
            RobieClientThread)

        assert isinstance(
            value,
            RobieClientThread)

        self.__thread = value


    @property
    def dumped(
        self,
    ) -> DictStrAny:
        """
        Return the facts about the attributes from the instance.

        :returns: Facts about the attributes from the instance.
        """

        dumped = super().dumped

        family = self.family

        return dumped | {
            'family': family}


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service threads.

        .. note::
           Deviates from enhomie in children have operations,
           and are more isolated from internal core routines.
        """

        raise NotImplementedError


    def get_message(
        self,
    ) -> 'RobieMessage':
        """
        Return the new item containing information for operation.

        :returns: New item containing information for operation.
        """

        raise NotImplementedError


    def put_message(
        self,
        mqueue: RobieQueue['RobieMessage'],
    ) -> None:
        """
        Insert the new item containing information for operation.

        :param mqueue: Queue instance where the item is received.
        """

        raise NotImplementedError


    def get_command(
        self,
    ) -> 'RobieCommand':
        """
        Return the new item containing information for operation.

        :returns: New item containing information for operation.
        """

        raise NotImplementedError


    def put_command(
        self,
        cqueue: RobieQueue['RobieCommand'],
    ) -> None:
        """
        Insert the new item containing information for operation.

        :param cqueue: Queue instance where the item is received.
        """

        raise NotImplementedError


    def compose(
        self,
        target: str,
        content: str,
    ) -> 'RobieCommand':
        """
        Compose the message and transmit using the chat client.

        :param target: Where the composed message will be sent.
        :param content: Content that will be source of message.
        """

        raise NotImplementedError
