"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import dumps
from pathlib import Path
from threading import Thread
from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.types import DictStrAny
from encommon.types import expate
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from enconnect.fixtures import MTMClientSocket
from enconnect.mattermost import ClientEvent
from enconnect.mattermost.test import EVENTS

from httpx import Response

from respx import MockRouter

from ..client import MTMClient
from ..command import MTMCommand
from ....conftest import config_factory
from ....conftest import robie_factory
from ....conftest import service_factory
from ....robie.addons import RobieQueue

if TYPE_CHECKING:
    from ....robie import Robie
    from ....robie import RobieService
    from ....robie.models import RobieCommand  # noqa: F401
    from ....robie.models import RobieMessage  # noqa: F401



MTMEVENT_RANDOM_CHAN = expate({
    'event': 'posted',
    'seq': 3,
    'broadcast/channel_id': 'enrobie',
    'data/channel_type': 'P',
    'data/post': (
        '{"user_id":"userid",'
        '"channel_id":"enrobie",'
        '"message":"Hello mtmbot"}'),
    'data/sender_name': '@user'})

MTMEVENT_RANDOM_PRIV = expate({
    'event': 'posted',
    'seq': 4,
    'broadcast/channel_id': 'privid',
    'data/channel_type': 'D',
    'data/post': (
        '{"user_id":"userid",'
        '"channel_id":"privid",'
        '"message":"Hello mtmbot"}'),
    'data/sender_name': '@user'})

MTMEVENT_HUBERT_CHAN = expate({
    'event': 'posted',
    'seq': 6,
    'broadcast/channel_id': 'enrobie',
    'data/channel_type': 'P',
    'data/post': (
        '{"user_id":"kjf9al2klaiietalkw",'
        '"channel_id":"enrobie",'
        '"message":"mtmbot"}'),
    'data/sender_name': '@hubert'})

MTMEVENT_HUBERT_PRIV = expate({
    'event': 'posted',
    'seq': 7,
    'broadcast/channel_id': 'privid',
    'data/channel_type': 'D',
    'data/post': (
        '{"user_id":"kjf9al2klaiietalkw",'
        '"channel_id":"privid",'
        '"message":"mtmbot"}'),
    'data/sender_name': '@hubert'})

_MTMEVENTS: list[DictStrAny] = [

    {'event': 'hello',
     'broadcast/user_id': 'mtmunq'},

    {'event': 'channel_updated',
     'broadcast/channel_id': 'enrobie',
     'data/channel': (
         '{"id":"enrobie",'
         '"name":"enrobie",'
         '"header":"Test topic is changed"}'),
     'seq': 2},

    # From random to channel
    MTMEVENT_RANDOM_CHAN,

    # From random to private
    MTMEVENT_RANDOM_PRIV,

    # From hubert to channel
    MTMEVENT_HUBERT_CHAN,

    # From hubert to channel
    MTMEVENT_HUBERT_CHAN,

    # From hubert to private
    MTMEVENT_HUBERT_PRIV,

    {'event': 'channel_updated',
     'broadcast/channel_id': 'enrobie',
     'data/channel': (
         '{"id":"enrobie",'
         '"name":"enrobie",'
         '"header":"Test topic"}'),
     'seq': 8}]

MTMEVENTS = EVENTS + [
    expate(x) for x in _MTMEVENTS]



def test_MTMClient(
    service: 'RobieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    """

    client = (
        service.clients
        .childs['mtmbot'])

    assert isinstance(
        client,
        MTMClient)


    attrs = lattrs(client)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params',
        '_MTMClient__client',
        '_MTMClient__channels',
        '_MTMClient__publish',
        '_RobieClient__thread']


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

    assert client.client

    assert client.channels

    assert client.publish

    assert client.schema()

    assert client.params

    assert client.thread

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



def test_MTMClient_channels(
    tmp_path: Path,
    client_mtmsock: MTMClientSocket,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param client_mtmsock: Object to mock client connection.
    :param respx_mock: Object for mocking request operation.
    """

    robie = robie_factory(
        config_factory(tmp_path))

    service = (
        service_factory(robie))


    childs = robie.childs
    clients = childs.clients

    client = clients['mtmbot']

    assert isinstance(
        client, MTMClient)


    mocked = dumps([
        {'header': 'Testing',
         'id': 'enrobie',
         'name': 'enrobie'}])

    (respx_mock
     .get(
         'https://mocked:443'
         '/api/v4/users/mtmunq/'
         'teams/mocked/channels')
     .mock(Response(
         status_code=200,
         content=mocked)))


    client_mtmsock(MTMEVENTS)


    service.limit(
        clients=['mtmbot'],
        plugins=['status'])

    service.start()


    thread = Thread(
        target=service.operate)

    thread.start()


    block_sleep(5)


    select = (
        client.channels
        .select('enrobie'))

    assert select is not None

    assert select.endumped == {
        'members': None,
        'title': 'enrobie',
        'topic': 'Test topic',
        'unique': 'enrobie'}


    service.soft()

    while service.running:
        block_sleep(1)

    service.stop()

    thread.join()
