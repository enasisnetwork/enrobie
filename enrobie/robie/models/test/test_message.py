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

from ..message import RobieMessage

if TYPE_CHECKING:
    from ...robie import Robie



def test_RobieMessage(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients
    client = clients['ircbot']

    model = RobieMessage


    item = model(client)


    attrs = lattrs(item)

    assert attrs == [
        'client',
        'time']


    assert inrepr(
        'RobieMessage',
        item)

    with raises(TypeError):
        assert hash(item) > 0

    assert instr(
        'RobieMessage',
        item)


    assert item.time.since > 0

    assert item.client == client.name
