"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Event
from time import sleep as block_sleep
from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Timer

from .members import RobieClients
from .members import RobiePlugins

if TYPE_CHECKING:
    from .robie import Robie
    from .params import RobieServiceParams



_CONGEST = list[tuple[str, int]]



class RobieService:
    """
    Multi-threaded service for processing the desired state.

    :param robie: Primary class instance for Chatting Robie.
    """

    __robie: 'Robie'

    __clients: RobieClients
    __plugins: RobiePlugins

    __timer: Timer
    __vacate: Event
    __cancel: Event
    __started: bool


    def __init__(
        self,
        robie: 'Robie',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        robie.logger.log_d(
            base=self,
            status='initial')

        self.__robie = robie

        self.__build_objects()

        self.__started = False

        robie.logger.log_i(
            base=self,
            status='created')


    def __build_objects(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params

        respite = params.respite


        self.__clients = (
            RobieClients(self))

        self.__plugins = (
            RobiePlugins(self))


        self.__timer = Timer(
            respite.health,
            start='min')

        self.__vacate = Event()
        self.__cancel = Event()


    @property
    def robie(
        self,
    ) -> 'Robie':
        """
        Return the Robie instance to which the instance belongs.

        :returns: Robie instance to which the instance belongs.
        """

        return self.__robie


    @property
    def params(
        self,
    ) -> 'RobieServiceParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        robie = self.__robie
        params = robie.params

        return params.service


    @property
    def clients(
        self,
    ) -> RobieClients:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__clients


    @property
    def plugins(
        self,
    ) -> RobiePlugins:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__plugins


    @property
    def running(
        self,
    ) -> list[str]:
        """
        Return the list of threads which are determined running.

        :returns: List of threads which are determined running.
        """

        running: list[str] = []

        clients = self.__clients
        plugins = self.__plugins

        running.extend(
            clients.running)

        running.extend(
            plugins.running)

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

        clients = self.__clients
        plugins = self.__plugins

        zombies.extend(
            clients.zombies)

        zombies.extend(
            plugins.zombies)

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

        clients = self.__clients
        plugins = self.__plugins

        congest.extend(
            clients.congest)

        congest.extend(
            plugins.congest)

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

        clients = self.__clients
        plugins = self.__plugins

        enqueue.extend(
            clients.enqueue)

        enqueue.extend(
            plugins.enqueue)

        return sorted(enqueue)


    def start(
        self,
    ) -> None:
        """
        Start the various threads within the Robie class object.
        """

        robie = self.__robie
        started = self.__started

        if started is True:
            return None

        self.__started = True

        robie.logger.log_i(
            base=self,
            status='starting')

        self.__plugins.start()
        self.__clients.start()

        robie.logger.log_i(
            base=self,
            status='started')


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service members.
        """

        robie = self.__robie

        clients = self.__clients
        plugins = self.__plugins

        while self.running:

            self.operate_clients()
            self.operate_plugins()

            clients.operate()
            plugins.operate()

            block_sleep(0.05)

            self.operate_healths()

        robie.logger.log_i(
            base=self,
            status='vacated')


    def operate_clients(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service members.
        """

        robie = self.__robie

        vacate = self.__vacate
        clients = self.__clients
        plugins = self.__plugins

        source = plugins.cqueue
        target = clients.cqueue


        while not source.empty:

            citem = source.get()

            if vacate.is_set():
                continue

            target.put(citem)

            robie.printer(citem)


    def operate_plugins(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service members.
        """

        robie = self.__robie

        vacate = self.__vacate
        clients = self.__clients
        plugins = self.__plugins

        source = clients.mqueue
        target = plugins.mqueue


        while not source.empty:

            mitem = source.get()

            if vacate.is_set():
                continue

            target.put(mitem)

            robie.printer(mitem)


    def operate_healths(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service members.
        """

        timer = self.__timer

        if timer.pause():
            return None

        vacate = self.__vacate
        cancel = self.__cancel

        self.check_congest()

        if vacate.is_set():
            return None

        if cancel.is_set():
            return None

        if self.check_zombies():
            self.stop()


    def check_zombies(
        self,
    ) -> bool:
        """
        Return the boolean indicating while threads are zombies.

        :returns: Boolean indicating while threads are zombies.
        """

        robie = self.__robie
        zombies = self.zombies

        for name in zombies:

            robie.logger.log_c(
                thread=name,
                status='zombie')

        return len(zombies) != 0


    def check_congest(
        self,
    ) -> bool:
        """
        Return the boolean indicating when queues are congested.

        :returns: Boolean indicating when queues are congested.
        """

        robie = self.__robie
        congest = self.congest

        for name, count in congest:

            robie.logger.log_e(
                queue=name,
                status='congest',
                count=count)

        return len(congest) != 0


    def soft(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Stop the various threads within the Robie class object.

        :param kwargs: Keyword arguments ignored by the method.
        :param args: Positional arguments ignored by the method.
        """

        robie = self.__robie
        started = self.__started
        vacate = self.__vacate

        if started is False:
            return None

        if vacate.is_set():
            return self.stop()

        robie.logger.log_i(
            base=self,
            status='vacating')

        vacate.set()

        self.__clients.stop()
        self.__plugins.soft()


    def stop(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Stop the various threads within the Robie class object.

        :param kwargs: Keyword arguments ignored by the method.
        :param args: Positional arguments ignored by the method.
        """

        robie = self.__robie
        started = self.__started
        vacate = self.__vacate
        cancel = self.__cancel

        if started is False:
            return None

        if cancel.is_set():
            return None

        vacate.set()
        cancel.set()

        robie.logger.log_i(
            base=self,
            status='stopping')

        self.__clients.stop()
        self.__plugins.stop()

        robie.logger.log_i(
            base=self,
            status='stopped')


    def limit(
        self,
        clients: Optional[list[str]] = None,
        plugins: Optional[list[str]] = None,
    ) -> None:
        """
        Remove the threads from members if not already started.

        :param clients: Names of the clients that are permitted.
        :param plugins: Names of the plugins that are permitted.
        """

        assert clients or plugins

        if plugins is not None:
            (self.__plugins
             .limit(plugins))

        if clients is not None:
            (self.__clients
             .limit(clients))
