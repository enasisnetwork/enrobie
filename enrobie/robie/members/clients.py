"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from .member import RobieMember
from ..threads import RobieClientThread

if TYPE_CHECKING:
    from .member import RobieThreads
    from ..childs import RobieClient  # noqa: F401



_CLIENTS = dict[str, 'RobieClient']



class RobieClients(RobieMember):
    """
    Common methods and routines for Chatting Robie members.
    """


    @property
    def childs(
        self,
    ) -> _CLIENTS:
        """
        Return the value for the attribute from class instance.

        .. note::
           Deviates from enhomie in build happens downstream,
           because all of the enhomie members are origin based
           where enrobie children do not have consistent base.

        :returns: Value for the attribute from class instance.
        """

        clients: _CLIENTS = {}

        threads = (
            self.threads
            .values())


        for thread in threads:

            assert isinstance(
                thread,
                RobieClientThread)

            client = thread.client
            name = client.name

            clients[name] = client


        return clients


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service members.
        """

        # Spread commands to clients

        robie = self.robie
        childs = robie.childs
        clients = childs.clients
        vacate = self.vacate
        cqueue = self.cqueue

        threads = (
            self.threads
            .values())


        def _put_command() -> None:

            child = thread.child
            _name = child.name

            if name != _name:
                return None

            (thread
             .cqueue.put(citem))


        while not cqueue.empty:

            citem = cqueue.get()

            if vacate.is_set():
                continue

            client = clients[
                citem.client]

            name = client.name

            for thread in threads:
                _put_command()


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

        robie = self.robie
        childs = robie.childs
        clients = childs.clients

        model = RobieClientThread


        threads: 'RobieThreads' = {}


        items = clients.items()

        for name, client in items:

            if not client.enable:
                continue  # NOCVR

            object = model(
                self, client)

            client.thread = object
            threads[name] = object


        self.threads = threads
