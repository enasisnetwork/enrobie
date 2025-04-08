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


    citem = RobieCommand(client)


    attrs = lattrs(citem)

    assert attrs == [
        'client',
        'time']


    assert inrepr(
        'RobieCommand',
        citem)

    with raises(TypeError):
        hash(citem)

    assert instr(
        'RobieCommand',
        citem)


    assert citem.time.since > 0

    assert citem.client == client.name
