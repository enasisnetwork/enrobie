"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from ..queue import RobieQueue
from ..queue import RobieQueueItem

if TYPE_CHECKING:
    from ...robie import Robie



def test_RobieQueueItem() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    item = RobieQueueItem()

    assert item.time.since < 1



def test_RobieQueue(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    _queue = RobieQueue[
        RobieQueueItem]

    item = RobieQueueItem()


    queue: _queue = (
        RobieQueue(robie))


    attrs = lattrs(queue)

    assert attrs == [
        '_RobieQueue__robie',
        '_RobieQueue__queue']


    assert inrepr(
        'queue.RobieQueue',
        queue)

    assert isinstance(
        hash(queue), int)

    assert instr(
        'queue.RobieQueue',
        queue)


    assert queue.empty

    assert queue.qsize == 0


    queue.put(item)

    assert not queue.empty

    assert queue.qsize == 1

    _item = queue.get()

    assert queue.empty

    assert queue.qsize == 0

    assert item == _item
