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
    from ..childs import RobiePlugin  # noqa: F401



_PLUGINS = dict[str, 'RobiePlugin']



class RobiePlugins(RobieMember):
    """
    Common methods and routines for Chatting Robie members.
    """


    @property
    def childs(
        self,
    ) -> _PLUGINS:
        """
        Return the value for the attribute from class instance.

        .. note::
           Deviates from enhomie in build happens downstream,
           because all of the enhomie members are origin based
           where enrobie children do not have consistent base.

        :returns: Value for the attribute from class instance.
        """

        plugins: _PLUGINS = {}

        threads = (
            self.threads
            .values())


        for thread in threads:

            assert isinstance(
                thread,
                RobiePluginThread)

            plugin = thread.plugin
            name = plugin.name

            plugins[name] = plugin


        return plugins


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Robie service members.
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

            if not plugin.enable:
                continue  # NOCVR

            object = model(
                self, plugin)

            plugin.thread = object
            threads[name] = object


        self.threads = threads
