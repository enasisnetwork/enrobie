"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from pathlib import Path
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

from httpx import Response

from respx import MockRouter

from ..plugin import HomiePlugin
from ....clients.discord.test import DSCEVENTS
from ....clients.discord.test import DSCEVENT_HUBERT_CHAN
from ....clients.discord.test import DSCEVENT_HUBERT_PRIV
from ....clients.irc.test import IRCEVENTS
from ....clients.irc.test import IRCEVENT_HUBERT_CHAN
from ....clients.irc.test import IRCEVENT_HUBERT_PRIV
from ....clients.mattermost.test import MTMEVENTS
from ....clients.mattermost.test import MTMEVENT_HUBERT_CHAN
from ....clients.mattermost.test import MTMEVENT_HUBERT_PRIV
from ....conftest import config_factory
from ....conftest import robie_factory
from ....conftest import service_factory

if TYPE_CHECKING:
    from ....robie import RobieService



def test_HomiePlugin(
    service: 'RobieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    """

    plugin = (
        service.plugins
        .childs['enhomie'])

    assert isinstance(
        plugin, HomiePlugin)


    attrs = lattrs(plugin)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params',
        '_HomiePlugin__started',
        '_HomiePlugin__persist',
        '_RobiePlugin__thread']


    assert inrepr(
        'plugin.HomiePlugin',
        plugin)

    assert isinstance(
        hash(plugin), int)

    assert instr(
        'plugin.HomiePlugin',
        plugin)


    plugin.validate()

    assert plugin.robie

    assert plugin.enable

    assert plugin.name == 'enhomie'

    assert plugin.kind == 'plugin'

    assert plugin.schema()

    assert plugin.params

    assert plugin.thread

    assert plugin.dumped

    assert plugin.persist



def test_HomiePlugin_cover(  # noqa: CFQ001
    tmp_path: Path,
    client_dscsock: DSCClientSocket,
    client_ircsock: IRCClientSocket,
    client_mtmsock: MTMClientSocket,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param client_dscsock: Object to mock client connection.
    :param client_ircsock: Object to mock client connection.
    :param client_mtmsock: Object to mock client connection.
    :param respx_mock: Object for mocking request operation.
    """

    robie = robie_factory(
        config_factory(tmp_path))

    service = (
        service_factory(robie))


    childs = robie.childs
    plugins = childs.plugins

    plugin = plugins['enhomie']

    assert isinstance(
        plugin, HomiePlugin)


    dscevents = (
        deepcopy(DSCEVENTS))

    dscchan = deepcopy(
        DSCEVENT_HUBERT_CHAN)

    dscpriv = deepcopy(
        DSCEVENT_HUBERT_PRIV)

    setate(
        dscchan,
        'd/content',
        '!persist unique')

    setate(
        dscpriv,
        'd/content',
        '!persist unique')

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
            ':!persist unique'))

    ircpriv = (
        ircpriv.replace(
            ':ircbot',
            ':!persist unique'))

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
             '!persist unique')))

    setate(
        mtmpriv, post,
        (getate(mtmpriv, post)
         .replace(
             'mtmbot',
             '!persist unique')))

    mtmevents.append(mtmpriv)
    mtmevents.append(mtmchan)

    client_mtmsock(mtmevents)


    (respx_mock
     .get(
         'https://mocked:8420'
         '/api/persists')
     .mock(Response(
         status_code=200)))


    client_dscsock(dscevents)
    client_ircsock(ircevents)
    client_mtmsock(mtmevents)


    service.limit(
        plugins=[
            'enhomie',
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
