"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from .common import AinswerTool

if TYPE_CHECKING:
    from .plugin import AinswerPlugin



class AinswerToolset:
    """
    Enumerate the plugins and return those that are related.

    :param plugin: Plugin class instance for Chatting Robie.
    """

    __plugin: 'AinswerPlugin'


    def __init__(
        self,
        plugin: 'AinswerPlugin',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__plugin = plugin


    @property
    def toolset(
        self,
    ) -> list[AinswerTool]:
        """
        Return the related tools that were found in the plugins.

        :returns: Related tools that were found in the plugins.
        """

        from .plugin import AinswerPlugin


        from .ainswer import (
            ainswer_memory_delete,
            ainswer_memory_insert,
            ainswer_memory_records)

        toolset: list[AinswerTool] = [
            ainswer_memory_insert,
            ainswer_memory_records,
            ainswer_memory_delete]


        plugin = self.__plugin

        if not plugin.thread:
            return toolset

        assert plugin.thread

        thread = plugin.thread
        params = plugin.params

        names = params.plugins

        if names is None:
            return toolset


        plugins = (
            thread.service
            .plugins.childs
            .values())

        for helper in plugins:

            name = helper.name

            if name not in names:
                continue

            ignored = isinstance(
                helper, AinswerPlugin)

            if ignored is True:
                continue

            related = hasattr(
                helper, 'ainswer')

            if related is False:
                continue

            assert hasattr(
                helper, 'ainswer')

            toolset.extend(
                helper.ainswer())


        return toolset
