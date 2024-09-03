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



class RobieClients(RobieMember):
    """
    Common methods and routines for Chatting Robie members.
    """


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
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

            object = model(
                self, client)

            threads[name] = object


        self.threads = threads
