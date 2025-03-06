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
from enconnect.discord.test import EVENTS

from pytest import raises

from ..client import DSCClient
from ..command import DSCCommand
from ..message import DSCMessage

if TYPE_CHECKING:
    from ....robie import Robie



def test_DSCMessage(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    model = DSCMessage

    client = clients['dscbot']

    assert isinstance(
        client, DSCClient)

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
        'DSCMessage',
        item)

    with raises(TypeError):
        hash(item)

    assert instr(
        'DSCMessage',
        item)


    assert item.time.since > 0

    assert item.client == client.name

    assert item.family == 'discord'

    assert item.kind == 'privmsg'

    assert not item.isme

    assert not item.hasme

    assert not item.whome

    assert item.author
    assert item.author[0] == 'user'

    assert item.message


    assert item.event == event

    assert event.type == (
        'MESSAGE_CREATE')
    assert event.opcode == 0
    assert event.data
    assert len(event.data) == 3
    assert event.seqno == 3
    assert len(event.original) == 4

    assert event.kind == 'privmsg'
    assert not event.isme
    assert not event.hasme
    assert not event.whome
    assert event.author == (
        'user', 'userid')
    assert event.recipient == (
        None, 'privid')
    assert event.message == (
        'Hello dscbot')



def test_DSCMessage_reply(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    model = DSCMessage

    client = clients['dscbot']

    assert isinstance(
        client, DSCClient)


    item = model(
        client,
        ClientEvent(
            client.client,
            EVENTS[0]))

    assert not item.isme


    reply = item.reply(
        robie, 'Hello')


    assert isinstance(
        reply, DSCCommand)


    assert reply.family == 'discord'

    assert reply.method == 'post'

    assert reply.path[-4:] == 'ages'

    assert not reply.params

    assert reply.json == {
        'content': 'Hello'}
