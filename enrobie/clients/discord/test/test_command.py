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

from ..command import DSCCommand

if TYPE_CHECKING:
    from ....robie import Robie



def test_DSCCommand(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    model = DSCCommand

    client = clients['ircbot']


    item = model(
        client, 'delete',
        '/channels/22220001'
        '/messages/33330001')


    attrs = lattrs(item)

    assert attrs == [
        'method',
        'path',
        'params',
        'json',
        'client',
        'time']


    assert inrepr(
        'DSCCommand',
        item)

    with raises(TypeError):
        assert hash(item) > 0

    assert instr(
        'DSCCommand',
        item)


    assert item.time.since > 0

    assert item.client == client.name

    assert item.family == 'discord'

    assert item.method == 'delete'

    assert item.path[-4:] == '0001'

    assert not item.params

    assert not item.json
