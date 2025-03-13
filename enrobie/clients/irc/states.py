"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ...utils import ClientChannel
from ...utils import ClientChannels as _ClientChannels



class ClientChannels(_ClientChannels):
    """
    Cache the information regarding client status on server.
    """


    def create(
        self,
        unique: str,
    ) -> None:
        """
        Create the channel within the internal cache dictionary.

        :param unique: Unique identifier for channel on server.
        """

        cached = self.__cached

        item = ClientChannel(
            unique=unique,
            title=unique)

        cached[unique] = item
