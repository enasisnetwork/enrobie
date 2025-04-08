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


    mitem = RobieMessage(client)


    attrs = lattrs(mitem)

    assert attrs == [
        'client',
        'person',
        'time']


    assert inrepr(
        'RobieMessage',
        mitem)

    with raises(TypeError):
        hash(mitem)

    assert instr(
        'RobieMessage',
        mitem)


    assert mitem.time.since > 0

    assert mitem.client == client.name
