"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import TYPE_CHECKING
from typing import Type

from encommon.types import DictStrAny

from .child import RobieChild
from ..addons import RobieQueue

if TYPE_CHECKING:
    from ..models import RobieCommand
    from ..models import RobieMessage
    from ..params import RobieClientParams



class RobieClient(RobieChild):
    """
    Establish and maintain connection with the chat service.
    """


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
