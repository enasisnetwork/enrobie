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
from enconnect.mattermost.test import EVENTS

from pytest import raises

from ..client import MTMClient
from ..command import MTMCommand
from ..message import MTMMessage

if TYPE_CHECKING:
    from ....robie import Robie



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

    client = clients['mtmbot']

    assert isinstance(
        client, MTMClient)

    event = ClientEvent(
        client.client,
        EVENTS[0])


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
        hash(item)

    assert instr(
        'MTMMessage',
        item)


    assert item.time.since > 0

    assert item.client == client.name

    assert item.family == 'mattermost'

    assert item.kind == 'privmsg'

    assert not item.isme

    assert not item.hasme

    assert not item.whome

    assert item.author
    assert item.author[0] == 'user'

    assert item.message


    assert item.event == event

    assert event.type == 'posted'
    assert event.data
    assert len(event.data) == 3
    assert event.broadcast
    assert len(event.broadcast) == 1
    assert event.seqno == 4
    assert not event.status
    assert not event.error
    assert not event.seqre

    assert event.kind == 'privmsg'
    assert not event.isme
    assert not event.hasme
    assert not event.whome
    assert event.author == (
        'user', 'userid')
    assert event.recipient == 'privid'
    assert event.message == (
        'Hello mtmbot')



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

    client = clients['mtmbot']

    assert isinstance(
        client, MTMClient)


    item = model(
        client,
        ClientEvent(
            client.client,
            EVENTS[0]))

    assert not item.isme


    reply = item.reply(
        robie, 'Hello')


    assert isinstance(
        reply, MTMCommand)


    assert reply.family == 'mattermost'

    assert reply.method == 'post'

    assert reply.path == 'posts'

    assert not reply.params

    assert reply.json == {
        'channel_id': 'privid',
        'message': 'Hello'}
