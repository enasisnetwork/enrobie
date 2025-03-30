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

from ..plugin import AinswerPlugin
from ....clients import IRCClient

if TYPE_CHECKING:
    from ....robie import Robie



def _ainswer_history(
    plugin: AinswerPlugin,
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
                author=f'nick{nick}',
                anchor='#enrobie',
                message=str(count),
                ainswer=str(count))

            history.insert(
                client=client.name,
                person=None,
                kind='privmsg',
                author=f'nick{nick}',
                anchor=f'nick{nick}',
                message=str(count),
                ainswer=str(count))

            block_sleep(0.001)


    history.insert(
        client=client.name,
        person='hubert',
        kind='chanmsg',
        author='hubert',
        anchor='#enrobie',
        message='Good news',
        ainswer='Everyone!')

    history.insert(
        client=client.name,
        person='hubert',
        kind='privmsg',
        author='hubert',
        anchor='hubert',
        message='Good news',
        ainswer='Everyone!')



def test_AinswerHistory(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    plugins = childs.plugins

    plugin = plugins['ainswer']

    assert isinstance(
        plugin, AinswerPlugin)


    history = plugin.history


    attrs = lattrs(history)

    assert attrs == [
        '_AinswerHistory__plugin',
        '_AinswerHistory__connect',
        '_AinswerHistory__locker',
        '_AinswerHistory__sengine',
        '_AinswerHistory__session']


    assert inrepr(
        'history.AinswerHistory',
        history)

    assert isinstance(
        hash(history), int)

    assert instr(
        'history.AinswerHistory',
        history)



def test_AinswerHistory_cover(
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
    plugin = plugins['ainswer']

    assert isinstance(
        client, IRCClient)

    assert isinstance(
        plugin, AinswerPlugin)

    history = plugin.history


    _ainswer_history(
        plugin, client)


    records = (
        history.search(
            client=client.name,
            anchor='#enrobie'))

    assert len(records) == 10


    record = (
        records[0].endumped)

    assert record == {
        'ainswer': '2',
        'anchor': '#enrobie',
        'author': 'nick4',
        'client': 'ircbot',
        'create': record['create'],
        'kind': 'chanmsg',
        'message': '2',
        'person': None,
        'plugin': 'ainswer'}


    records = (
        history.search(
            client=client.name,
            anchor='nick1'))

    record = (
        records[-1].endumped)

    assert record == {
        'ainswer': '4',
        'anchor': 'nick1',
        'author': 'nick1',
        'client': 'ircbot',
        'create': record['create'],
        'kind': 'privmsg',
        'message': '4',
        'person': None,
        'plugin': 'ainswer'}


    records = (
        history.search(
            client=client.name,
            author='nick1',
            anchor='nick1',
            limit=1))

    assert len(records) == 1
