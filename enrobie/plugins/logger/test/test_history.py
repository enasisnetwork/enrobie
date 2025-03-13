"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from ..plugin import LoggerPlugin
from ....clients import IRCClient

if TYPE_CHECKING:
    from ....robie import Robie



def _logger_history(
    plugin: LoggerPlugin,
    client: 'IRCClient',
) -> None:
    """
    Insert testing records into the provided history object.

    :param plugin: Plugin class instance for Chatting Robie.
    :param client: Client class instance for Chatting Robie.
    """

    history = plugin.history


    for count in range(4):

        count += 1

        for nick in range(4):

            nick += 1

            history.insert(
                client=client.name,
                person=None,
                kind='chanmsg',
                author=f'nickname{nick}',
                anchor='#enrobie',
                message=f'Message {count}')

            history.insert(
                client=client.name,
                person=None,
                kind='privmsg',
                author=f'nickname{nick}',
                anchor=f'nickname{nick}',
                message=f'Message {count}')

            block_sleep(0.001)


    history.insert(
        client=client.name,
        person='hubert',
        kind='chanmsg',
        author='hubert',
        anchor='#enrobie',
        message='Good news')

    history.insert(
        client=client.name,
        person='hubert',
        kind='privmsg',
        author='hubert',
        anchor='hubert',
        message='Good news')



def test_LoggerHistory(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    plugins = childs.plugins

    plugin = plugins['logger']

    assert isinstance(
        plugin, LoggerPlugin)


    history = plugin.history


    attrs = lattrs(history)

    assert attrs == [
        '_LoggerHistory__plugin',
        '_LoggerHistory__connect',
        '_LoggerHistory__locker',
        '_LoggerHistory__sengine',
        '_LoggerHistory__session']


    assert inrepr(
        'history.LoggerHistory',
        history)

    assert isinstance(
        hash(history), int)

    assert instr(
        'history.LoggerHistory',
        history)



def test_LoggerHistory_cover(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients
    plugins = childs.plugins

    client = clients['ircbot']
    plugin = plugins['logger']

    assert isinstance(
        client, IRCClient)

    assert isinstance(
        plugin, LoggerPlugin)

    history = plugin.history


    _logger_history(
        plugin, client)


    records = (
        history.search(
            client=client.name,
            anchor='#enrobie'))

    assert len(records) == 10


    record = (
        records[0].endumped)

    assert record == {
        'anchor': '#enrobie',
        'author': 'nickname4',
        'client': 'ircbot',
        'create': record['create'],
        'kind': 'chanmsg',
        'message': 'Message 2',
        'person': None,
        'plugin': 'logger'}


    records = (
        history.search(
            client=client.name,
            anchor='nickname1'))

    record = (
        records[-1].endumped)

    assert record == {
        'anchor': 'nickname1',
        'author': 'nickname1',
        'client': 'ircbot',
        'create': record['create'],
        'kind': 'privmsg',
        'message': 'Message 4',
        'person': None,
        'plugin': 'logger'}


    records = (
        history.search(
            client=client.name,
            author='nickname1',
            anchor='nickname1',
            limit=1))

    assert len(records) == 1


    plaintext = (
        history.plaintext(
            client=client.name,
            anchor='nickname1'))

    plain = plaintext[-1]

    assert plain[27:] == (
        '<nickname1> Message 4')
