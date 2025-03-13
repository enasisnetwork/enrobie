"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from pytest import raises

from ..command import RobieCommand

if TYPE_CHECKING:
    from ...robie import Robie



def test_RobieCommand(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients
    client = clients['ircbot']


    item = RobieCommand(client)


    attrs = lattrs(item)

    assert attrs == [
        'client',
        'time']


    assert inrepr(
        'RobieCommand',
        item)

    with raises(TypeError):
        hash(item)

    assert instr(
        'RobieCommand',
        item)


    assert item.time.since > 0

    assert item.client == client.name
