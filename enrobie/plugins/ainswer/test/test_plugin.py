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

from enconnect.discord.test import EVENTS as DSCEVENTS
from enconnect.fixtures import DSCClientSocket
from enconnect.fixtures import IRCClientSocket
from enconnect.fixtures import MTMClientSocket
from enconnect.irc.test import EVENTS as IRCEVENTS
from enconnect.mattermost.test import EVENTS as MTMEVENTS

from pydantic_ai.models.test import TestModel

from ..plugin import AinswerPlugin

if TYPE_CHECKING:
    from ....robie import Robie
    from ....robie import RobieService



def test_AinswerPlugin(
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


    attrs = lattrs(plugin)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params',
        '_AinswerPlugin__history',
        '_AinswerPlugin__model',
        '_AinswerPlugin__agent']


    assert inrepr(
        'plugin.AinswerPlugin',
        plugin)

    assert isinstance(
        hash(plugin), int)

    assert instr(
        'plugin.AinswerPlugin',
        plugin)


    plugin.validate()

    assert plugin.robie

    assert plugin.enable

    assert plugin.name == 'ainswer'

    assert plugin.kind == 'plugin'

    assert plugin.schema()

    assert plugin.params

    assert plugin.dumped



def test_AinswerPlugin_cover(
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

    robie = service.robie
    childs = robie.childs
    plugins = childs.plugins

    plugin = plugins['ainswer']

    assert isinstance(
        plugin, AinswerPlugin)


    client_dscsock(DSCEVENTS)
    client_ircsock(IRCEVENTS)
    client_mtmsock(MTMEVENTS)


    testing = TestModel()

    override_agent = (
        plugin.agent
        .override(
            model=testing))

    with override_agent:


        service.limit_threads(
            plugins=['ainswer'])

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
