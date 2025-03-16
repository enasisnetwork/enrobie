"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from threading import Thread
from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import read_text

from enconnect.fixtures import DSCClientSocket
from enconnect.fixtures import IRCClientSocket
from enconnect.fixtures import MTMClientSocket

from ..plugin import LoggerPlugin
from ....clients.discord.test import DSCEVENTS
from ....clients.irc.test import IRCEVENTS
from ....clients.mattermost.test import MTMEVENTS

if TYPE_CHECKING:
    from ....robie import RobieService



def test_LoggerPlugin(
    service: 'RobieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    """

    plugin = (
        service.plugins
        .childs['logger'])

    assert isinstance(
        plugin, LoggerPlugin)


    attrs = lattrs(plugin)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params',
        '_LoggerPlugin__started',
        '_LoggerPlugin__history',
        '_RobiePlugin__thread']


    assert inrepr(
        'plugin.LoggerPlugin',
        plugin)

    assert isinstance(
        hash(plugin), int)

    assert instr(
        'plugin.LoggerPlugin',
        plugin)


    plugin.validate()

    assert plugin.robie

    assert plugin.enable

    assert plugin.name == 'logger'

    assert plugin.kind == 'plugin'

    assert plugin.schema()

    assert plugin.params

    assert plugin.thread

    assert plugin.dumped



def test_LoggerPlugin_cover(
    service: 'RobieService',
    client_dscsock: DSCClientSocket,
    client_ircsock: IRCClientSocket,
    client_mtmsock: MTMClientSocket,
    tmp_path: Path,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    :param client_dscsock: Object to mock client connection.
    :param client_ircsock: Object to mock client connection.
    :param client_mtmsock: Object to mock client connection.
    :param tmp_path: pytest object for temporal filesystem.
    """

    plugin = (
        service.plugins
        .childs['logger'])

    assert isinstance(
        plugin, LoggerPlugin)

    plugin.params.output = (
        f'{tmp_path}/output.txt')


    client_dscsock(DSCEVENTS)
    client_ircsock(IRCEVENTS)
    client_mtmsock(MTMEVENTS)


    service.limit(
        plugins=[
            'logger',
            'status'])

    service.start()


    thread = Thread(
        target=service.operate)

    thread.start()


    block_sleep(5)

    service.soft()

    while service.running:
        block_sleep(1)

    service.stop()

    thread.join()


    content = read_text(
        f'{tmp_path}/output.txt')

    assert 'Hello dscbot' in content
    assert 'Hello ircbot' in content
    assert 'Hello mtmbot' in content
