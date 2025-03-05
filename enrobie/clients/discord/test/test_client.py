"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from enconnect.discord import ClientEvent

from ..client import DSCClient
from ..command import DSCCommand
from ....robie.addons import RobieQueue

if TYPE_CHECKING:
    from ....robie import Robie
    from ....robie.models import RobieCommand  # noqa: F401
    from ....robie.models import RobieMessage  # noqa: F401



def test_DSCClient(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients


    client = clients['dscbot']

    assert isinstance(
        client,
        DSCClient)


    attrs = lattrs(client)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params',
        '_DSCClient__client']


    assert inrepr(
        'client.DSCClient',
        client)

    assert isinstance(
        hash(client), int)

    assert instr(
        'client.DSCClient',
        client)


    client.validate()

    assert client.robie

    assert client.enable

    assert client.name == 'dscbot'

    assert client.family == 'discord'

    assert client.kind == 'client'

    assert client.schema()

    assert client.params

    assert client.dumped



def test_DSCClient_message(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    client = clients['dscbot']

    assert isinstance(
        client, DSCClient)


    _queue = RobieQueue[
        'RobieMessage']

    queue: _queue = (
        RobieQueue(robie))


    _event = {'op': 7}

    event = ClientEvent(
        client.client, _event)

    client.put_message(
        queue, event)



def test_DSCClient_command(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    client = clients['dscbot']

    assert isinstance(
        client, DSCClient)


    _queue = RobieQueue[
        'RobieCommand']

    queue: _queue = (
        RobieQueue(robie))


    client.put_command(
        queue, 'delete',
        'channels/privid/'
        'messages/msgunq')



def test_DSCClient_compose(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    client = clients['dscbot']

    assert isinstance(
        client, DSCClient)


    citem = (
        client.compose(
            'chan', 'message'))

    assert isinstance(
        citem, DSCCommand)


    assert citem.method == 'post'

    assert citem.path == (
        'channels/chan/messages')

    assert not citem.params

    assert citem.json == {
        'content': 'message'}
