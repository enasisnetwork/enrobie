"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from threading import Thread
from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils.sample import ENPYRWS

from enconnect.fixtures import IRCClientSocket
from enconnect.irc import ClientEvent

from pytest import raises

from . import SAMPLES
from .test_client import IRCEVENTS
from .test_client import IRCEVENT_HUBERT_CHAN
from .test_client import IRCEVENT_RANDOM_CHAN
from .test_client import IRCEVENT_RANDOM_PRIV
from ..client import IRCClient
from ..command import IRCCommand
from ..message import IRCMessage

if TYPE_CHECKING:
    from ....robie import Robie
    from ....robie import RobieService
    from ....robie.models import RobieMessage



def test_IRCMessage(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    client = clients['ircbot']

    assert isinstance(
        client, IRCClient)


    item = IRCMessage(
        client,
        ClientEvent(
            client.client,
            IRCEVENT_HUBERT_CHAN))


    attrs = lattrs(item)

    assert attrs == [
        'event',
        'client',
        'person',
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

    assert item.kind == 'chanmsg'

    assert item.person == 'hubert'

    assert not item.isme

    assert not item.hasme

    assert not item.whome

    assert item.author
    assert item.author[0] == 'hubert'

    assert item.anchor == '#enrobie'

    assert item.message


    event = item.event

    assert event.prefix == (
        'hubert!hubert@science.com')
    assert event.command == 'PRIVMSG'
    assert event.params
    assert len(event.params) == 16
    assert len(event.original) == 51

    assert event.kind == 'chanmsg'
    assert not event.isme
    assert not event.hasme
    assert not event.whome
    assert event.author == 'hubert'
    assert event.recipient == '#enrobie'
    assert event.message == 'ircbot'



def test_IRCMessage_reply(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    client = clients['ircbot']

    assert isinstance(
        client, IRCClient)


    item = IRCMessage(
        client,
        ClientEvent(
            client.client,
            IRCEVENT_RANDOM_CHAN))

    reply = item.reply(
        robie, 'Hello')

    assert isinstance(
        reply, IRCCommand)

    assert reply.event == (
        'PRIVMSG #enrobie :Hello')


    item = IRCMessage(
        client,
        ClientEvent(
            client.client,
            IRCEVENT_RANDOM_PRIV))

    reply = item.reply(
        robie, 'Hello')

    assert isinstance(
        reply, IRCCommand)

    assert reply.event == (
        'PRIVMSG nick :Hello')



def test_IRCMessage_samples(
    tmp_path: Path,
    service: 'RobieService',
    client_ircsock: IRCClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param service: Ancilary Chatting Robie class instance.
    :param client_ircsock: Object to mock client connection.
    """

    robie = service.robie
    childs = robie.childs
    clients = childs.clients

    client = clients['ircbot']

    assert isinstance(
        client, IRCClient)


    messages: list[IRCMessage] = []


    def _callback(
        mitem: 'RobieMessage',
    ) -> None:

        assert isinstance(
            mitem, IRCMessage)

        messages.append(mitem)


    (client.publish
     .subscribe(_callback))


    client_ircsock(IRCEVENTS)

    service.limit(
        clients=['ircbot'],
        plugins=['status'])

    service.start()


    thread = Thread(
        target=service.operate)

    thread.start()


    block_sleep(5)


    sample_path = (
        SAMPLES / 'messages.json')

    # Because of ones in helper
    maximum = len(IRCEVENTS) + 4

    _messages = [
        {'client': x.client,
         'family': x.family,
         'kind': x.kind,
         'person': x.person,
         'isme': x.isme,
         'hasme': x.hasme,
         'whome': x.whome,
         'author': x.author,
         'anchor': x.anchor,
         'message': x.message,
         'event': x.event}
        for x in
        messages[:maximum]]

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=_messages)

    expect = prep_sample(
        content=_messages)

    assert expect == sample


    service.soft()

    while service.running:
        block_sleep(1)

    service.stop()

    thread.join()
