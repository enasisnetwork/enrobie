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

from enconnect.fixtures import MTMClientSocket
from enconnect.mattermost import ClientEvent

from pytest import raises

from . import SAMPLES
from .test_client import MTMEVENTS
from .test_client import MTMEVENT_HUBERT_CHAN
from .test_client import MTMEVENT_RANDOM_CHAN
from .test_client import MTMEVENT_RANDOM_PRIV
from ..client import MTMClient
from ..command import MTMCommand
from ..message import MTMMessage

if TYPE_CHECKING:
    from ....robie import Robie
    from ....robie import RobieService
    from ....robie.models import RobieMessage



def test_MTMMessage(
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


    item = MTMMessage(
        client,
        ClientEvent(
            client.client,
            MTMEVENT_HUBERT_CHAN))


    attrs = lattrs(item)

    assert attrs == [
        'event',
        'client',
        'person',
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

    assert item.kind == 'chanmsg'

    assert item.person == 'hubert'

    assert not item.isme

    assert not item.hasme

    assert not item.whome

    assert item.author
    assert item.author[0] == 'hubert'

    assert item.anchor == 'enrobie'

    assert item.message


    event = item.event

    assert event.type == 'posted'
    assert event.data
    assert len(event.data) == 3
    assert event.broadcast
    assert len(event.broadcast) == 1
    assert event.seqno == 6
    assert not event.status
    assert not event.error
    assert not event.seqre

    assert event.kind == 'chanmsg'
    assert not event.isme
    assert not event.hasme
    assert not event.whome
    assert event.author == (
        'hubert', 'kjf9al2klaiietalkw')
    assert event.recipient == 'enrobie'
    assert event.message == 'mtmbot'



def test_MTMMessage_reply(
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


    item = MTMMessage(
        client,
        ClientEvent(
            client.client,
            MTMEVENT_RANDOM_CHAN))

    reply = item.reply(
        robie, 'Hello')

    assert isinstance(
        reply, MTMCommand)

    assert reply.json == {
        'channel_id': 'enrobie',
        'message': 'Hello'}


    item = MTMMessage(
        client,
        ClientEvent(
            client.client,
            MTMEVENT_RANDOM_PRIV))

    reply = item.reply(
        robie, 'Hello')

    assert isinstance(
        reply, MTMCommand)

    assert reply.json == {
        'channel_id': 'privid',
        'message': 'Hello'}



def test_MTMMessage_samples(
    tmp_path: Path,
    service: 'RobieService',
    client_mtmsock: MTMClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param service: Ancilary Chatting Robie class instance.
    :param client_mtmsock: Object to mock client connection.
    """

    robie = service.robie
    childs = robie.childs
    clients = childs.clients

    client = clients['mtmbot']

    assert isinstance(
        client, MTMClient)


    messages: list[MTMMessage] = []


    def _callback(
        mitem: 'RobieMessage',
    ) -> None:

        assert isinstance(
            mitem, MTMMessage)

        messages.append(mitem)


    (client.publish
     .subscribe(_callback))


    client_mtmsock(MTMEVENTS)

    service.limit(
        clients=['mtmbot'],
        plugins=['status'])

    service.start()


    thread = Thread(
        target=service.operate)

    thread.start()


    block_sleep(5)


    sample_path = (
        SAMPLES / 'messages.json')

    # Because of ones in helper
    maximum = len(MTMEVENTS) + 5

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
