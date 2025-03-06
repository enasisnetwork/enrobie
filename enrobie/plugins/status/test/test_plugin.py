"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from threading import Thread
from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.types import getate
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.types import setate

from enconnect.discord.test import EVENTS as DSCEVENTS
from enconnect.fixtures import DSCClientSocket
from enconnect.fixtures import IRCClientSocket
from enconnect.fixtures import MTMClientSocket
from enconnect.irc.test import EVENTS as IRCEVENTS
from enconnect.mattermost.test import EVENTS as MTMEVENTS

from ..plugin import StatusPlugin

if TYPE_CHECKING:
    from ....robie import Robie
    from ....robie import RobieService



DSCEVENTS = deepcopy(DSCEVENTS)
IRCEVENTS = deepcopy(IRCEVENTS)
MTMEVENTS = deepcopy(MTMEVENTS)



setate(
    DSCEVENTS[0],
    'd/content',
    '!status')

setate(
    DSCEVENTS[1],
    'd/content',
    '!status')



IRCEVENTS[1] = (
    IRCEVENTS[1]
    .replace(
        'Hello ircbot',
        '!status'))

IRCEVENTS[3] = (
    IRCEVENTS[3]
    .replace(
        'Hello world',
        '!status'))



setate(
    MTMEVENTS[0],
    'data/post',
    (getate(
        MTMEVENTS[0],
        'data/post')
     .replace(
         'Hello mtmbot',
         '!status')))

setate(
    MTMEVENTS[1],
    'data/post',
    (getate(
        MTMEVENTS[1],
        'data/post')
     .replace(
         'Hello world',
         '!status')))



def test_StatusPlugin(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    plugins = childs.plugins


    plugin = plugins['status']

    assert isinstance(
        plugin, StatusPlugin)


    attrs = lattrs(plugin)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params',
        '_StatusPlugin__status',
        '_StatusPlugin__stated']


    assert inrepr(
        'plugin.StatusPlugin',
        plugin)

    assert isinstance(
        hash(plugin), int)

    assert instr(
        'plugin.StatusPlugin',
        plugin)


    plugin.validate()

    assert plugin.robie

    assert plugin.enable

    assert plugin.name == 'status'

    assert plugin.kind == 'plugin'

    assert plugin.schema()

    assert plugin.params

    assert plugin.dumped



def test_StatusPlugin_cover(
    service: 'RobieService',
    client_dscsock: DSCClientSocket,
    client_ircsock: IRCClientSocket,
    client_mtmsock: MTMClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    :param client_dscsock: Object to mock client connection.
    :param client_ircsock: Object to mock client connection.
    :param client_mtmsock: Object to mock client connection.
    """

    client_dscsock(DSCEVENTS)
    client_ircsock(IRCEVENTS)
    client_mtmsock(MTMEVENTS)

    service.limit_threads(
        plugins=['status'])

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
