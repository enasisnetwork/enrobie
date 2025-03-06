"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from enconnect.irc import ClientEvent
from enconnect.irc.test import EVENTS

from pytest import raises

from ..client import IRCClient
from ..command import IRCCommand
from ..message import IRCMessage

if TYPE_CHECKING:
    from ....robie import Robie



def test_IRCMessage(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    model = IRCMessage

    client = clients['ircbot']

    assert isinstance(
        client, IRCClient)

    event = ClientEvent(
        client.client,
        EVENTS[1])


    item = model(
        client, event)


    attrs = lattrs(item)

    assert attrs == [
        'event',
        'client',
        'time']


    assert inrepr(
        'IRCMessage',
        item)

    with raises(TypeError):
        hash(item)

    assert instr(
        'IRCMessage',
        item)


    assert item.time.since > 0

    assert item.client == client.name

    assert item.family == 'irc'

    assert item.kind == 'privmsg'

    assert not item.isme

    assert not item.hasme

    assert not item.whome

    assert item.author
    assert item.author[0] == 'nick'

    assert item.message


    assert item.event == event

    assert event.prefix == (
        'nick!user@host')
    assert event.command == 'PRIVMSG'
    assert event.params
    assert len(event.params) == 20
    assert len(event.original) == 44

    assert event.kind == 'privmsg'
    assert not event.isme
    assert not event.hasme
    assert not event.whome
    assert event.author == 'nick'
    assert event.recipient == 'ircbot'
    assert event.message == (
        'Hello ircbot')



def test_IRCMessage_reply(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    model = IRCMessage

    client = clients['ircbot']

    assert isinstance(
        client, IRCClient)


    item = model(
        client,
        ClientEvent(
            client.client,
            EVENTS[1]))

    assert not item.isme


    reply = item.reply(
        robie, 'Hello')


    event = ClientEvent(
        client.client,
        EVENTS[1].replace(
            '#channel',
            'ircbot'))

    item = model(
        client, event)

    reply = item.reply(
        robie, 'Hello')


    assert isinstance(
        reply, IRCCommand)


    assert reply.event == (
        'PRIVMSG nick :Hello')
