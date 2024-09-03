"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from .member import RobieMember
from ..threads import RobiePluginThread

if TYPE_CHECKING:
    from .member import RobieThreads



class RobiePlugins(RobieMember):
    """
    Common methods and routines for Chatting Robie members.
    """


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        vacate = self.vacate
        mqueue = self.mqueue

        threads = (
            self.threads
            .values())


        def _put_message() -> None:

            (thread
             .mqueue.put(mitem))


        while not mqueue.empty:

            mitem = mqueue.get()

            if vacate.is_set():
                continue

            for thread in threads:
                _put_message()


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
        plugins = childs.plugins

        model = RobiePluginThread


        threads: 'RobieThreads' = {}


        items = plugins.items()

        for name, plugin in items:

            object = model(
                self, plugin)

            threads[name] = object


        self.threads = threads
