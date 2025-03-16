"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread
from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from enconnect.fixtures import IRCClientSocket
from enconnect.irc import ClientEvent
from enconnect.irc.test import EVENTS

from ..client import IRCClient
from ..command import IRCCommand
from ....robie.addons import RobieQueue

if TYPE_CHECKING:
    from ....robie import Robie
    from ....robie import RobieService
    from ....robie.models import RobieCommand  # noqa: F401
    from ....robie.models import RobieMessage  # noqa: F401



IRCEVENT_RANDOM_CHAN = (
    ':nick!user@host PRIVMSG'
    ' #enrobie :Hello ircbot')

IRCEVENT_RANDOM_PRIV = (
    ':nick!user@host PRIVMSG'
    ' ircbot :Hello ircbot')

IRCEVENT_HUBERT_CHAN = (
    ':hubert!hubert@science.com'
    ' PRIVMSG #enrobie :ircbot')

IRCEVENT_HUBERT_PRIV = (
    ':hubert!hubert@science.com'
    ' PRIVMSG ircbot :ircbot')

IRCEVENTS: list[str] = [

    *EVENTS[:-1],

    (':botirc!user@host'
     ' NICK :ircbot'),

    ':ircbot JOIN :#enrobie',

    (':mocked 353 ircbot = #enrobie'
     ' :ircbot robert trebor sirrah'),

    (':mocked 332 ircbot #enrobie'
     ' :Test topic already set'),

    (':nick!user@host TOPIC #enrobie'
     ' :Test topic is changed'),

    (':nick!user@host KICK '
     '#enrobie ircbot :foo'),

    ':ircbot JOIN :#enrobie',

    (':mocked 353 ircbot = #enrobie'
     ' :ircbot robert trebor sirrah'),

    (':mocked 332 ircbot #enrobie'
     ' :Test topic is changed'),

    # From random to channel
    IRCEVENT_RANDOM_CHAN,

    # From random to private
    IRCEVENT_RANDOM_PRIV,

    # From hubert to channel
    IRCEVENT_HUBERT_CHAN,

    # From hubert to channel
    IRCEVENT_HUBERT_CHAN,

    # From hubert to private
    IRCEVENT_HUBERT_PRIV,

    (':nick!user@host TOPIC #enrobie'
     ' :Test topic'),

    (':trebor!user@host NICK treb0r'),

    (':nick!user@host NICK n1ck'),

    ':ircbot PART :#enrobie']



def test_IRCClient(
    service: 'RobieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    """

    client = (
        service.clients
        .childs['ircbot'])

    assert isinstance(
        client,
        IRCClient)


    attrs = lattrs(client)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params',
        '_IRCClient__client',
        '_IRCClient__channels',
        '_IRCClient__publish',
        '_RobieClient__thread']


    assert inrepr(
        'client.IRCClient',
        client)

    assert isinstance(
        hash(client), int)

    assert instr(
        'client.IRCClient',
        client)


    client.validate()

    assert client.robie

    assert client.enable

    assert client.name == 'ircbot'

    assert client.family == 'irc'

    assert client.kind == 'client'

    assert client.client

    assert client.channels

    assert client.publish

    assert client.schema()

    assert client.params

    assert client.thread

    assert client.dumped



def test_IRCClient_message(
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


    _queue = RobieQueue[
        'RobieMessage']

    queue: _queue = (
        RobieQueue(robie))


    _event = 'PING :123456789'

    event = ClientEvent(
        client.client, _event)

    client.put_message(
        queue, event)



def test_IRCClient_command(
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


    _queue = RobieQueue[
        'RobieCommand']

    queue: _queue = (
        RobieQueue(robie))


    client.put_command(
        queue,
        'PRIVMSG # :Hello')



def test_IRCClient_compose(
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


    citem = (
        client.compose(
            '#enrobie',
            'message'))

    assert isinstance(
        citem, IRCCommand)


    assert citem.event == (
        'PRIVMSG #enrobie'
        ' :message')



def test_IRCClient_channels(
    service: 'RobieService',
    client_ircsock: IRCClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    :param client_ircsock: Object to mock client connection.
    """

    robie = service.robie
    childs = robie.childs
    clients = childs.clients

    client = clients['ircbot']

    assert isinstance(
        client, IRCClient)


    client_ircsock(IRCEVENTS)


    service.limit(
        clients=['ircbot'],
        plugins=['status'])

    service.start()


    thread = Thread(
        target=service.operate)

    thread.start()


    block_sleep(5)


    select = (
        client.channels
        .select('#enrobie'))

    assert select is not None

    assert select.endumped == {
        'members': {
            'robert',
            'sirrah',
            'treb0r'},
        'title': '#enrobie',
        'topic': 'Test topic',
        'unique': '#enrobie'}


    service.soft()

    while service.running:
        block_sleep(1)

    service.stop()

    thread.join()
