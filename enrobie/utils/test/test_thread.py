"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread
from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from ..thread import DupliThread

if TYPE_CHECKING:
    from ...robie import Robie



def test_DupliThread() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    raises = DupliThread(
        thread='invalid')


    attrs = lattrs(raises)

    assert attrs == [
        'thread',
        'about']


    assert inrepr(
        'DupliThread',
        raises)

    assert isinstance(
        hash(raises), int)

    assert instr(
        'Thread (invalid)',
        raises)


    assert str(raises) == (
        'Thread (invalid) '
        'would be duplicate')



def test_DupliThread_cover(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    thread = Thread(
        name='client')


    raises = DupliThread(
        thread=thread,
        about='about')

    assert str(raises) == (
        'Thread (client) '
        'would be duplicate'
        ' (about)')
