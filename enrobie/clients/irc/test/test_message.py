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

from pytest import raises

from ..command import IRCCommand
from ..message import IRCMessage

if TYPE_CHECKING:
    from ....robie import Robie



EVENT = (
    ':n!u@h PRIVMSG #chan'
    ' :Hello channel')



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

    event = ClientEvent(EVENT)

    client = clients['ircbot']


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
        assert hash(item) > 0

    assert instr(
        'IRCMessage',
        item)


    assert item.time.since > 0

    assert item.client == client.name

    assert item.family == 'irc'

    assert item.kind == 'event'

    assert item.event == event


    assert event.prefix == 'n!u@h'
    assert event.command == 'PRIVMSG'
    assert event.params
    assert len(event.params) == 20
    assert len(event.original) == 35

    assert event.kind == 'chanmsg'
    assert event.author == 'n'
    assert event.recipient == '#chan'
    assert event.message == (
        'Hello channel')



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


    item = model(
        clients['ircbot'],
        ClientEvent(EVENT))

    reply = item.reply(
        robie, 'Hello')


    event = ClientEvent(
        EVENT.replace(
            '#chan', 'ircbot'))

    client = clients['ircbot']

    item = model(
        client, event)

    reply = item.reply(
        robie, 'Hello')


    assert isinstance(
        reply, IRCCommand)


    assert reply.event == (
        'PRIVMSG n :Hello')
