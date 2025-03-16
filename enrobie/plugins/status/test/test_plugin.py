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

from enconnect.fixtures import DSCClientSocket
from enconnect.fixtures import IRCClientSocket
from enconnect.fixtures import MTMClientSocket

from ..plugin import StatusPlugin
from ....clients.discord.test import DSCEVENTS
from ....clients.discord.test import DSCEVENT_HUBERT_CHAN
from ....clients.discord.test import DSCEVENT_HUBERT_PRIV
from ....clients.irc.test import IRCEVENTS
from ....clients.irc.test import IRCEVENT_HUBERT_CHAN
from ....clients.irc.test import IRCEVENT_HUBERT_PRIV
from ....clients.mattermost.test import MTMEVENTS
from ....clients.mattermost.test import MTMEVENT_HUBERT_CHAN
from ....clients.mattermost.test import MTMEVENT_HUBERT_PRIV

if TYPE_CHECKING:
    from ....robie import RobieService



def test_StatusPlugin(
    service: 'RobieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    """

    plugin = (
        service.plugins
        .childs['status'])

    assert isinstance(
        plugin, StatusPlugin)


    attrs = lattrs(plugin)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params',
        '_StatusPlugin__status',
        '_StatusPlugin__stated',
        '_RobiePlugin__thread']


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

    assert plugin.thread

    assert plugin.dumped

    assert not plugin.status



def test_StatusPlugin_cover(  # noqa: CFQ001
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


    dscevents = (
        deepcopy(DSCEVENTS))

    dscchan = deepcopy(
        DSCEVENT_HUBERT_CHAN)

    dscpriv = deepcopy(
        DSCEVENT_HUBERT_PRIV)

    setate(
        dscchan,
        'd/content',
        '!status')

    setate(
        dscpriv,
        'd/content',
        '!status')

    dscevents.append(dscpriv)
    dscevents.append(dscchan)

    client_dscsock(dscevents)


    ircevents = (
        deepcopy(IRCEVENTS))

    ircchan = (
        IRCEVENT_HUBERT_CHAN)

    ircpriv = (
        IRCEVENT_HUBERT_PRIV)

    ircchan = (
        ircchan.replace(
            ':ircbot',
            ':!status'))

    ircpriv = (
        ircpriv.replace(
            ':ircbot',
            ':!status'))

    ircevents.append(ircpriv)
    ircevents.append(ircchan)

    client_ircsock(ircevents)


    mtmevents = (
        deepcopy(MTMEVENTS))

    mtmchan = deepcopy(
        MTMEVENT_HUBERT_CHAN)

    mtmpriv = deepcopy(
        MTMEVENT_HUBERT_PRIV)

    post = 'data/post'

    setate(
        mtmchan, post,
        (getate(mtmchan, post)
         .replace(
             'mtmbot',
             '!status')))

    setate(
        mtmpriv, post,
        (getate(mtmpriv, post)
         .replace(
             'mtmbot',
             '!status')))

    mtmevents.append(mtmpriv)
    mtmevents.append(mtmchan)

    client_mtmsock(mtmevents)


    service.limit(
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
