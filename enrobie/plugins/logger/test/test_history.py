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

if TYPE_CHECKING:
    from ....robie.childs import RobieClient
    from ....robie import Robie



def _insert_history(
    plugin: LoggerPlugin,
    client: 'RobieClient',
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
                client,
                f'nickname{nick}',
                '#channel',
                f'Message {count}')

            history.insert(
                client,
                f'nickname{nick}',
                f'nickname{nick}',
                f'Message {count}')

            block_sleep(0.001)



def test_LoggerHistory(
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


    _insert_history(
        plugin, client)


    records = (
        history.records(
            client,
            '#channel'))

    assert len(records) == 10


    record = (
        records[0].endumped)

    assert record == {
        'anchor': '#channel',
        'author': 'nickname3',
        'client': 'ircbot',
        'create': record['create'],
        'message': 'Message 2',
        'plugin': 'logger'}


    records = (
        history.records(
            client,
            'nickname1'))

    record = (
        records[-1].endumped)

    assert record == {
        'anchor': 'nickname1',
        'author': 'nickname1',
        'client': 'ircbot',
        'create': record['create'],
        'message': 'Message 4',
        'plugin': 'logger'}


    plaintext = (
        history.plaintext(
            client,
            'nickname1'))

    plain = plaintext[-1]

    assert plain[27:] == (
        '<nickname1> Message 4')
