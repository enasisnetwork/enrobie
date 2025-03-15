"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from .thread import RobieThread

if TYPE_CHECKING:
    from ..childs import RobiePlugin
    from ..members import RobiePlugins



class RobiePluginThread(RobieThread):
    """
    Common methods and routines for Chatting Robie threads.
    """


    @property
    def member(
        self,
    ) -> 'RobiePlugins':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        from ..members import (
            RobiePlugins)

        member = super().member

        assert isinstance(
            member, RobiePlugins)

        return member


    @property
    def child(
        self,
    ) -> 'RobiePlugin':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        from ..childs import (
            RobiePlugin)

        child = super().child

        assert isinstance(
            child, RobiePlugin)

        return child


    @property
    def plugin(
        self,
    ) -> 'RobiePlugin':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.child
