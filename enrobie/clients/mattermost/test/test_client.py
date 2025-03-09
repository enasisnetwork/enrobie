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
    from ....robie.models import RobieCommand  # noqa: F401
    from ....robie.models import RobieMessage  # noqa: F401



MTMEVENTS: list[DictStrAny] = [

    {'event': 'hello',
     'broadcast': {
         'user_id': 'mtmunq'}},

    {'event': 'posted',
     'seq': 5,
     'broadcast': {
         'channel_id': 'chanid'},
     'data/channel_type': 'P',
     'data/post': (
         '{"user_id":"userid",'
         '"channel_id":"chanid",'
         '"message":"Hello mtmbot"}'),
     'data/sender_name': '@user'},

    {'event': 'channel_updated',
     'broadcast': {
         'channel_id': 'mtmunq'},
     'data/channel': (
         '{"id":"mtmunq",'
         '"name":"testing",'
         '"header":"Testing"}'),
     'seq': 2}]

MTMEVENTS = EVENTS + [
    expate(x) for x in MTMEVENTS]



def test_MTMClient(
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
        client,
        MTMClient)


    attrs = lattrs(client)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params',
        '_MTMClient__client',
        '_MTMClient__channels']


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

    assert client.schema()

    assert client.params

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


    content = [
        {'header': 'Testing',
         'id': 'mtmunq',
         'name': 'testing'}]


    (respx_mock
     .get(
         'https://mocked:443'
         '/api/v4/users/mtmunq/'
         'teams/mocked/channels')
     .mock(Response(
         status_code=200,
         content=dumps(content))))


    client_mtmsock(MTMEVENTS)

    service.limit_threads(
        clients=['mtmbot'],
        plugins=['status'])

    service.start()


    thread = Thread(
        target=service.operate)

    thread.start()


    block_sleep(5)


    select = (
        client.channels
        .select('mtmunq'))

    assert select is not None

    assert select.endumped == {
        'members': None,
        'title': 'testing',
        'topic': 'Testing',
        'unique': 'mtmunq'}


    service.soft()

    while service.running:
        block_sleep(1)

    service.stop()

    thread.join()
