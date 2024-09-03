"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal

from .child import RobieChild



class RobiePlugin(RobieChild):
    """
    Integrate with the Robie routine and perform operations.
    """


    @property
    def kind(
        self,
    ) -> Literal['plugin']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'plugin'
