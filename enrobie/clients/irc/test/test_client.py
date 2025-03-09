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

    ':ircbot JOIN :#test',

    (':mocked 353 ircbot = #test '
     ':ircbot robert trebor sirrah'),

    (':mocked 332 ircbot #test '
     ':Test topic already set'),

    (':foo!bar@baz KICK '
     '#test ircbot :foo'),

    ':ircbot JOIN :#test',

    (':mocked 353 ircbot = #test '
     ':ircbot robert trebor sirrah'),

    (':mocked 332 ircbot #test '
     ':Test topic already set'),

    (':foo!bar@baz TOPIC #test '
     ':Test topic is changed'),

    (':nick!user@host PRIVMSG'
     ' #test :Hello ircbot'),

    ':ircbot PART :#test']

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
            '#channel',
            'message'))

    assert isinstance(
        citem, IRCCommand)


    assert citem.event == (
        'PRIVMSG #channel'
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
        .select('#test'))

    assert select is not None

    assert select.endumped == {
        'members': {
            'robert',
            'sirrah',
            'trebor'},
        'title': '#test',
        'topic': 'Test topic is changed',
        'unique': '#test'}


    service.soft()

    while service.running:
        block_sleep(1)

    service.stop()

    thread.join()
