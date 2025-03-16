"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread
from time import sleep as block_sleep
from typing import TYPE_CHECKING
from typing import Union

from encommon.types import clsname

from ..addons import RobieQueue
from ...utils import DupliThread

if TYPE_CHECKING:
    from ..common import RobieOperate
    from ..members import RobieMember
    from ..models import RobieCommand
    from ..models import RobieMessage
    from ..robie import Robie
    from ..service import RobieService



_CONGEST = list[tuple[str, int]]



RobieThreadItems = Union[
    'RobieMessage',
    'RobieCommand']



class RobieThread(Thread):
    """
    Common methods and routines for Chatting Robie threads.

    :param member: Child class instance for Chatting Robie.
    :param child: Child class instance for Chatting Robie.
    """

    __member: 'RobieMember'
    __child: 'RobieOperate'

    __mqueue: RobieQueue['RobieMessage']
    __cqueue: RobieQueue['RobieCommand']


    def __init__(
        self,
        member: 'RobieMember',
        child: 'RobieOperate',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        robie = member.robie

        super().__init__()

        self.name = (
            f'{clsname(self)}'
            f'/{child.name}')

        robie.logger.log_d(
            base=self,
            name=child,
            status='initial')

        self.__member = member
        self.__child = child

        self.__build_objects()

        robie.logger.log_i(
            base=self,
            name=child,
            status='created')


    def __build_objects(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        member = self.__member
        robie = member.robie

        self.__mqueue = (
            RobieQueue(robie))

        self.__cqueue = (
            RobieQueue(robie))


    @property
    def robie(
        self,
    ) -> 'Robie':
        """
        Return the Robie instance to which the instance belongs.

        :returns: Robie instance to which the instance belongs.
        """

        return self.member.robie


    @property
    def service(
        self,
    ) -> 'RobieService':
        """
        Return the Robie instance to which the instance belongs.

        :returns: Robie instance to which the instance belongs.
        """

        return self.__member.service


    @property
    def member(
        self,
    ) -> 'RobieMember':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__member


    @property
    def child(
        self,
    ) -> 'RobieOperate':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__child


    @property
    def mqueue(
        self,
    ) -> RobieQueue['RobieMessage']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__mqueue


    @property
    def cqueue(
        self,
    ) -> RobieQueue['RobieCommand']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__cqueue


    def expired(
        self,
        item: RobieThreadItems,
    ) -> bool:
        """
        Return the boolean indicating whether the item expired.

        :param item: Item containing information for operation.
        :returns: Boolean indicating whether the item expired.
        """

        member = self.member
        robie = member.robie

        since = item.time.since
        client = item.client

        if since < 60:
            return False

        robie.logger.log_w(
            base=self,
            item=item,
            client=client,
            status='expired',
            age=int(since))

        return True


    @property
    def congest(
        self,
    ) -> _CONGEST:
        """
        Return the list of congested threads and members queues.

        :returns: List of congested threads and members queues.
        """

        congest: _CONGEST = []

        name = self.name

        mqueue = self.mqueue
        cqueue = self.cqueue


        if mqueue.qsize > 5:

            append = (
                f'{name}/mqueue',
                mqueue.qsize)

            congest.append(append)

        if cqueue.qsize > 5:

            append = (
                f'{name}/cqueue',
                cqueue.qsize)

            congest.append(append)


        return sorted(congest)


    @property
    def enqueue(
        self,
    ) -> _CONGEST:
        """
        Return the list of congested threads and members queues.

        :returns: List of congested threads and members queues.
        """

        enqueue: _CONGEST = []

        name = self.name

        mqueue = self.mqueue
        cqueue = self.cqueue


        if mqueue.qsize > 0:

            append = (
                f'{name}/mqueue',
                mqueue.qsize)

            enqueue.append(append)

        if cqueue.qsize > 0:

            append = (
                f'{name}/cqueue',
                cqueue.qsize)

            enqueue.append(append)


        return sorted(enqueue)


    def run(
        self,
    ) -> None:
        """
        Perform whatever operation is associated with the class.
        """

        member = self.__member
        child = self.__child
        robie = member.robie
        vacate = member.vacate
        cancel = member.cancel

        robie.logger.log_i(
            base=self,
            name=child,
            status='started')


        def _continue() -> bool:

            if cancel.is_set():
                return False

            enqueue = bool(
                self.enqueue)

            if vacate.is_set():
                return enqueue

            return True


        while _continue():

            self.operate()

            block_sleep(0.1)


        robie.logger.log_i(
            base=self,
            name=child,
            status='stopped')


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service threads.
        """

        member = self.__member
        child = self.__child
        robie = member.robie
        vacate = member.vacate

        try:
            child.operate()

        except DupliThread as reason:

            vacate.set()

            robie.logger.log_e(
                base=self,
                name=child,
                status='exception',
                exc_info=reason)

            block_sleep(15)

        except Exception as reason:

            robie.logger.log_e(
                base=self,
                name=child,
                status='exception',
                exc_info=reason)

            block_sleep(1)


    def stop(
        self,
    ) -> None:
        """
        Wait for the thread object to complete routine and exit.
        """

        member = self.__member
        child = self.__child
        robie = member.robie

        robie.logger.log_d(
            base=self,
            name=child,
            status='waiting')

        self.join()

        robie.logger.log_d(
            base=self,
            name=child,
            status='awaited')
