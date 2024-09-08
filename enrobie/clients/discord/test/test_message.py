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

from pytest import raises

from ..command import DSCCommand
from ..message import DSCMessage

if TYPE_CHECKING:
    from ....robie import Robie



EVENT = {
    't': 'MESSAGE_CREATE',
    's': 3,
    'op': 0,
    'd': {
        'id': '33330001',
        'channel_id': '22220001',
        'author': {
            'id': '44444444',
            'username': 'Author'},
        'content': 'Hello person'}}



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
        'DSCMessage',
        item)

    with raises(TypeError):
        assert hash(item) > 0

    assert instr(
        'DSCMessage',
        item)


    assert item.time.since > 0

    assert item.client == client.name

    assert item.family == 'discord'

    assert item.kind == 'privmsg'

    assert item.event == event


    assert event.type == (
        'MESSAGE_CREATE')
    assert event.opcode == 0
    assert event.data
    assert len(event.data) == 4
    assert event.seqno == 3
    assert len(event.original) == 4

    assert event.kind == 'privmsg'
    assert event.author == (
        '44444444', 'Author')
    assert event.recipient == (
        None, '22220001')
    assert event.message == (
        'Hello person')



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


    item = model(
        clients['dscbot'],
        ClientEvent(EVENT))

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
