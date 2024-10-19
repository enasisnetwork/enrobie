"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread
from typing import Optional



class DupliThread(Exception):
    """
    Exception for when the client thread is already running.

    :param thread: Name or thread that would be duplicative.
    :param about: Additional information for the exception.
    """

    thread: str
    about: Optional[str] = None


    def __init__(
        self,
        thread: str | Thread,
        about: Optional[str] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        if hasattr(thread, 'name'):
            thread = thread.name

        message = (
            f'Thread ({thread}) '
            'would be duplicate')

        if about is not None:
            message += (
                f' ({about})')

        self.thread = thread
        self.about = about

        super().__init__(message)
