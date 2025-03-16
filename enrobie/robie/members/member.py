"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Event
from typing import TYPE_CHECKING

from encommon.types import clsname

from ..addons import RobieQueue
from ..threads import RobieThread  # noqa: F401

if TYPE_CHECKING:
    from ..models import RobieCommand
    from ..models import RobieMessage
    from ..robie import Robie
    from ..service import RobieService



RobieThreads = dict[str, 'RobieThread']

_CONGEST = list[tuple[str, int]]



class RobieMember:
    """
    Common methods and routines for Chatting Robie members.

    :param robie: Primary class instance for Chatting Robie.
    """

    __service: 'RobieService'

    __threads: RobieThreads

    __mqueue: RobieQueue['RobieMessage']
    __cqueue: RobieQueue['RobieCommand']
    __vacate: Event
    __cancel: Event


    def __init__(
        self,
        service: 'RobieService',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        robie = service.robie

        robie.logger.log_d(
            base=self,
            status='initial')

        self.__service = service

        self.__threads = {}

        self.__build_objects()

        robie.logger.log_i(
            base=self,
            status='created')


    def __build_objects(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        robie = self.robie

        self.__mqueue = (
            RobieQueue(robie))

        self.__cqueue = (
            RobieQueue(robie))

        self.__vacate = Event()
        self.__cancel = Event()

        self.build_threads()


    def build_threads(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.

        .. note::
           Deviates from enhomie in build happens downstream,
           because all of the enhomie members are origin based
           where enrobie children do not have consistent base.
        """

        raise NotImplementedError


    def limit(
        self,
        names: list[str],
    ) -> None:
        """
        Remove the thread from member when not already started.

        .. note::
           Deviates from enhomie in build happens downstream,
           because all of the enhomie members are origin based
           where enrobie children do not have consistent base.

        :param names: Names of the children that are permitted.
        """

        threads = self.__threads

        for name in list(threads):

            thread = threads[name]

            if name in names:
                continue

            assert not thread.ident

            del threads[name]


    @property
    def robie(
        self,
    ) -> 'Robie':
        """
        Return the Robie instance to which the instance belongs.

        :returns: Robie instance to which the instance belongs.
        """

        return self.__service.robie


    @property
    def service(
        self,
    ) -> 'RobieService':
        """
        Return the Robie instance to which the instance belongs.

        :returns: Robie instance to which the instance belongs.
        """

        return self.__service


    @property
    def threads(
        self,
    ) -> RobieThreads:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        threads = self.__threads

        return dict(threads)


    @threads.setter
    def threads(
        self,
        value: RobieThreads,
    ) -> None:
        """
        Update the value for the attribute from class instance.
        """

        self.__threads = value


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


    @property
    def vacate(
        self,
    ) -> Event:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__vacate


    @property
    def cancel(
        self,
    ) -> Event:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__cancel


    @property
    def running(
        self,
    ) -> list[str]:
        """
        Return the list of threads which are determined running.

        :returns: List of threads which are determined running.
        """

        running: list[str] = []

        threads = (
            self.__threads
            .values())

        for thread in threads:

            if not thread.is_alive():
                continue

            name = thread.name

            running.append(name)

        return sorted(running)


    @property
    def zombies(
        self,
    ) -> list[str]:
        """
        Return the list of threads which are determined zombies.

        :returns: List of threads which are determined zombies.
        """

        zombies: list[str] = []

        threads = (
            self.__threads
            .values())

        for thread in threads:

            if thread.is_alive():
                continue

            name = thread.name

            zombies.append(name)

        return sorted(zombies)


    @property
    def congest(
        self,
    ) -> _CONGEST:
        """
        Return the list of congested threads and members queues.

        :returns: List of congested threads and members queues.
        """

        congest: _CONGEST = []

        name = clsname(self)

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


        threads = (
            self.__threads
            .values())

        for thread in threads:

            congest.extend(
                thread.congest)


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

        name = clsname(self)

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


        threads = (
            self.__threads
            .values())

        for thread in threads:

            enqueue.extend(
                thread.enqueue)


        return sorted(enqueue)


    def start(
        self,
    ) -> None:
        """
        Start the various threads within the Robie class object.
        """

        threads = (
            self.__threads
            .values())

        for thread in threads:
            thread.start()


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service members.
        """

        raise NotImplementedError


    def soft(
        self,
    ) -> None:
        """
        Stop the various threads within the Robie class object.
        """

        self.__vacate.set()


    def stop(
        self,
    ) -> None:
        """
        Stop the various threads within the Robie class object.
        """

        self.__vacate.set()
        self.__cancel.set()

        threads = (
            self.__threads
            .values())

        for thread in threads:
            thread.stop()
