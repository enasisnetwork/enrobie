"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from enconnect.mattermost import ClientEvent

from ..client import MTMClient
from ..command import MTMCommand
from ....robie.addons import RobieQueue

if TYPE_CHECKING:
    from ....robie import Robie
    from ....robie.models import RobieCommand  # noqa: F401
    from ....robie.models import RobieMessage  # noqa: F401



def test_MTMClient(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients


    client = clients['mtmbot']

    assert isinstance(
        client,
        MTMClient)


    attrs = lattrs(client)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params',
        '_MTMClient__client']


    assert inrepr(
        'client.MTMClient',
        client)

    assert isinstance(
        hash(client), int)

    assert instr(
        'client.MTMClient',
        client)


    client.validate()

    assert client.robie

    assert client.enable

    assert client.name == 'mtmbot'

    assert client.family == 'mattermost'

    assert client.kind == 'client'

    assert client.schema()

    assert client.params

    assert client.dumped



def test_MTMClient_message(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    client = clients['mtmbot']

    assert isinstance(
        client, MTMClient)


    _queue = RobieQueue[
        'RobieMessage']

    queue: _queue = (
        RobieQueue(robie))


    _event = {
        'status': 'OK',
        'seq_reply': 1}

    event = ClientEvent(
        client.client, _event)

    client.put_message(
        queue, event)



def test_MTMClient_command(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    client = clients['mtmbot']

    assert isinstance(
        client, MTMClient)


    _queue = RobieQueue[
        'RobieCommand']

    queue: _queue = (
        RobieQueue(robie))


    client.put_command(
        queue, 'delete',
        'posts/mocked')



def test_MTMClient_compose(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    client = clients['mtmbot']

    assert isinstance(
        client, MTMClient)


    citem = (
        client.compose(
            'chan', 'message'))

    assert isinstance(
        citem, MTMCommand)


    assert citem.method == 'post'

    assert citem.path == 'posts'

    assert not citem.params

    assert citem.json == {
        'channel_id': 'chan',
        'message': 'message'}
