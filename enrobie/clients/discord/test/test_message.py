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

from enconnect.discord import ClientEvent
from enconnect.fixtures import DSCClientSocket

from pytest import raises

from . import SAMPLES
from .test_client import DSCEVENTS
from .test_client import DSCEVENT_HUBERT_CHAN
from .test_client import DSCEVENT_RANDOM_CHAN
from .test_client import DSCEVENT_RANDOM_PRIV
from ..client import DSCClient
from ..command import DSCCommand
from ..message import DSCMessage

if TYPE_CHECKING:
    from ....robie import Robie
    from ....robie import RobieService
    from ....robie.models import RobieMessage



def test_DSCMessage(
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


    item = DSCMessage(
        client,
        ClientEvent(
            client.client,
            DSCEVENT_HUBERT_CHAN))


    attrs = lattrs(item)

    assert attrs == [
        'event',
        'client',
        'person',
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

    assert item.kind == 'chanmsg'

    assert item.person == 'hubert'

    assert not item.isme

    assert not item.hasme

    assert not item.whome

    assert item.author
    assert item.author[0] == 'hubert'

    assert item.anchor == 'guildid:enrobie'

    assert item.message


    event = item.event

    assert event.type == (
        'MESSAGE_CREATE')
    assert event.opcode == 0
    assert event.data
    assert len(event.data) == 4
    assert event.seqno == 7
    assert len(event.original) == 4

    assert event.kind == 'chanmsg'
    assert not event.isme
    assert not event.hasme
    assert not event.whome
    assert event.author == (
        'hubert', '823039201390230492')
    assert event.recipient == (
        'guildid', 'enrobie')
    assert event.message == 'dscbot'



def test_DSCMessage_reply(
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


    item = DSCMessage(
        client,
        ClientEvent(
            client.client,
            DSCEVENT_RANDOM_CHAN))

    reply = item.reply(
        robie, 'Hello')

    assert isinstance(
        reply, DSCCommand)

    assert reply.json == {
        'content': 'Hello'}


    item = DSCMessage(
        client,
        ClientEvent(
            client.client,
            DSCEVENT_RANDOM_PRIV))

    reply = item.reply(
        robie, 'Hello')

    assert isinstance(
        reply, DSCCommand)

    assert reply.json == {
        'content': 'Hello'}



def test_DSCMessage_samples(
    tmp_path: Path,
    service: 'RobieService',
    client_dscsock: DSCClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param service: Ancilary Chatting Robie class instance.
    :param client_dscsock: Object to mock client connection.
    """

    robie = service.robie
    childs = robie.childs
    clients = childs.clients

    client = clients['dscbot']

    assert isinstance(
        client, DSCClient)


    messages: list[DSCMessage] = []


    def _callback(
        mitem: 'RobieMessage',
    ) -> None:

        assert isinstance(
            mitem, DSCMessage)

        messages.append(mitem)


    (client.publish
     .subscribe(_callback))


    client_dscsock(DSCEVENTS)

    service.limit(
        clients=['dscbot'],
        plugins=['status'])

    service.start()


    thread = Thread(
        target=service.operate)

    thread.start()


    block_sleep(5)


    sample_path = (
        SAMPLES / 'messages.json')

    # Because of ones in helper
    maximum = len(DSCEVENTS) + 4

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
