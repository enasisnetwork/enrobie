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

from pytest import raises

from ..command import MTMCommand
from ..message import MTMMessage

if TYPE_CHECKING:
    from ....robie import Robie



EVENT = {
    'event': 'posted',
    'seq': 5,
    'broadcast': {
        'channel_id': 'nwyxekd4k7'},
    'data': {
        'channel_type': 'P',
        'post': (
            '{"user_id":"ietyrmdt5b",'
            '"channel_id":"nwyxekd4k7",'
            '"message":"Hello"}'),
        'sender_name': '@robert'}}



def test_MTMMessage(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    model = MTMMessage

    event = ClientEvent(EVENT)

    client = clients['mtmbot']


    item = model(
        client, event)


    attrs = lattrs(item)

    assert attrs == [
        'event',
        'client',
        'time']


    assert inrepr(
        'MTMMessage',
        item)

    with raises(TypeError):
        assert hash(item) > 0

    assert instr(
        'MTMMessage',
        item)


    assert item.time.since > 0

    assert item.client == client.name

    assert item.family == 'mattermost'

    assert item.kind == 'chanmsg'

    assert item.event == event


    assert event.type == 'posted'
    assert event.data
    assert len(event.data) == 3
    assert event.broadcast
    assert len(event.broadcast) == 1
    assert event.seqno == 5
    assert not event.status
    assert not event.error
    assert not event.seqre

    assert event.kind == 'chanmsg'
    assert event.author == (
        'ietyrmdt5b', '@robert')
    assert event.recipient == 'nwyxekd4k7'
    assert event.message == 'Hello'



def test_MTMMessage_reply(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    model = MTMMessage


    item = model(
        clients['mtmbot'],
        ClientEvent(EVENT))

    reply = item.reply(
        robie, 'Hello')


    assert isinstance(
        reply, MTMCommand)


    assert reply.family == 'mattermost'

    assert reply.method == 'post'

    assert reply.path == 'posts'

    assert not reply.params

    assert reply.json == {
        'channel_id': 'nwyxekd4k7',
        'message': 'Hello'}
