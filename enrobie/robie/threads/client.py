"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from .thread import RobieThread

if TYPE_CHECKING:
    from ..childs import RobieClient
    from ..members import RobieClients



class RobieClientThread(RobieThread):
    """
    Common methods and routines for Chatting Robie threads.
    """


    @property
    def member(
        self,
    ) -> 'RobieClients':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        from ..members import (
            RobieClients)

        member = super().member

        assert isinstance(
            member, RobieClients)

        return member


    @property
    def child(
        self,
    ) -> 'RobieClient':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        from ..childs import (
            RobieClient)

        child = super().child

        assert isinstance(
            child, RobieClient)

        return child


    @property
    def client(
        self,
    ) -> 'RobieClient':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.child
