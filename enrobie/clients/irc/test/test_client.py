"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from enconnect.irc import ClientEvent

from ..client import IRCClient
from ..command import IRCCommand
from ....robie.addons import RobieQueue

if TYPE_CHECKING:
    from ....robie import Robie
    from ....robie.models import RobieCommand  # noqa: F401
    from ....robie.models import RobieMessage  # noqa: F401



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
        '_IRCClient__client']


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
