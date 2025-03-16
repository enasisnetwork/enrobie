"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread
from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.types import DictStrAny
from encommon.types import expate
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from enconnect.discord import ClientEvent
from enconnect.discord.test import EVENTS
from enconnect.fixtures import DSCClientSocket

from ..client import DSCClient
from ..command import DSCCommand
from ....robie.addons import RobieQueue

if TYPE_CHECKING:
    from ....robie import Robie
    from ....robie import RobieService
    from ....robie.models import RobieCommand  # noqa: F401
    from ....robie.models import RobieMessage  # noqa: F401



DSCEVENT_RANDOM_CHAN = expate({
    't': 'MESSAGE_CREATE',
    's': 4,
    'op': 0,
    'd/channel_id': 'enrobie',
    'd/guild_id': 'guildid',
    'd/author/id': 'userid',
    'd/author/username': 'user',
    'd/content': 'Hello dscbot'})

DSCEVENT_RANDOM_PRIV = expate({
    't': 'MESSAGE_CREATE',
    's': 5,
    'op': 0,
    'd/channel_id': 'privid',
    'd/author/id': 'userid',
    'd/author/username': 'user',
    'd/content': 'Hello dscbot'})

DSCEVENT_HUBERT_CHAN = expate({
    't': 'MESSAGE_CREATE',
    's': 7,
    'op': 0,
    'd/channel_id': 'enrobie',
    'd/guild_id': 'guildid',
    'd/author/id': '823039201390230492',
    'd/author/username': 'hubert',
    'd/content': 'dscbot'})

DSCEVENT_HUBERT_PRIV = expate({
    't': 'MESSAGE_CREATE',
    's': 8,
    'op': 0,
    'd/channel_id': 'privid',
    'd/author/id': '823039201390230492',
    'd/author/username': 'hubert',
    'd/content': 'dscbot'})

DSCEVENTS: list[DictStrAny] = [

    {'t': 'GUILD_CREATE',
     's': 2,
     'op': 0,
     'd/channels/0': {
         'id': 'enrobie',
         'topic': 'Test topic already set',
         'name': 'enrobie'}},

    {'t': 'CHANNEL_UPDATE',
     's': 3,
     'op': 0,
     'd/id': 'enrobie',
     'd/topic': 'Test topic is changed',
     'd/name': 'enrobie'},

    # From random to channel
    DSCEVENT_RANDOM_CHAN,

    # From random to private
    DSCEVENT_RANDOM_PRIV,

    # From hubert to channel
    DSCEVENT_HUBERT_CHAN,

    # From hubert to channel
    DSCEVENT_HUBERT_CHAN,

    # From hubert to private
    DSCEVENT_HUBERT_PRIV,

    {'t': 'CHANNEL_UPDATE',
     's': 9,
     'op': 0,
     'd/id': 'enrobie',
     'd/topic': 'Test topic',
     'd/name': 'enrobie'}]

DSCEVENTS = EVENTS + [
    expate(x) for x in DSCEVENTS]



def test_DSCClient(
    service: 'RobieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    """

    client = (
        service.clients
        .childs['dscbot'])

    assert isinstance(
        client,
        DSCClient)


    attrs = lattrs(client)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params',
        '_DSCClient__client',
        '_DSCClient__channels',
        '_DSCClient__publish',
        '_RobieClient__thread']


    assert inrepr(
        'client.DSCClient',
        client)

    assert isinstance(
        hash(client), int)

    assert instr(
        'client.DSCClient',
        client)


    client.validate()

    assert client.robie

    assert client.enable

    assert client.name == 'dscbot'

    assert client.family == 'discord'

    assert client.kind == 'client'

    assert client.client

    assert client.channels

    assert client.publish

    assert client.schema()

    assert client.params

    assert client.thread

    assert client.dumped



def test_DSCClient_message(
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


    _queue = RobieQueue[
        'RobieMessage']

    queue: _queue = (
        RobieQueue(robie))


    _event = {'op': 7}

    event = ClientEvent(
        client.client, _event)

    client.put_message(
        queue, event)



def test_DSCClient_command(
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


    _queue = RobieQueue[
        'RobieCommand']

    queue: _queue = (
        RobieQueue(robie))


    client.put_command(
        queue, 'delete',
        'channels/privid/'
        'messages/msgunq')



def test_DSCClient_compose(
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


    citem = (
        client.compose(
            'chan', 'message'))

    assert isinstance(
        citem, DSCCommand)


    assert citem.method == 'post'

    assert citem.path == (
        'channels/chan/messages')

    assert not citem.params

    assert citem.json == {
        'content': 'message'}



def test_DSCClient_channels(
    service: 'RobieService',
    client_dscsock: DSCClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    :param client_dscsock: Object to mock client connection.
    """

    robie = service.robie
    childs = robie.childs
    clients = childs.clients

    client = clients['dscbot']

    assert isinstance(
        client, DSCClient)


    client_dscsock(DSCEVENTS)


    service.limit(
        clients=['dscbot'],
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
