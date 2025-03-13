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



IRCEVENTS: list[str] = [

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
    (':nick!user@host PRIVMSG'
     ' #enrobie :Hello ircbot'),

    # From random to private
    (':nick!user@host PRIVMSG'
     ' ircbot :Hello ircbot'),

    # From hubert to channel
    (':hubert!hubert@science.com'
     ' PRIVMSG #enrobie :ircbot'),

    # From hubert to channel
    (':hubert!hubert@science.com'
     ' PRIVMSG #enrobie :ircbot'),

    # From hubert to private
    (':hubert!hubert@science.com'
     ' PRIVMSG ircbot :ircbot'),

    ':ircbot PART :#enrobie']

IRCEVENTS.extend(EVENTS[:-1])



def test_IRCClient(
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
        client,
        IRCClient)


    attrs = lattrs(client)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params',
        '_IRCClient__client',
        '_IRCClient__channels']


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

    assert client.schema()

    assert client.params

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

    service.limit_threads(
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
            'trebor'},
        'title': '#enrobie',
        'topic': 'Test topic is changed',
        'unique': '#enrobie'}


    service.soft()

    while service.running:
        block_sleep(1)

    service.stop()

    thread.join()
