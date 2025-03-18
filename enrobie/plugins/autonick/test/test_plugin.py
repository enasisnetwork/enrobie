"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from threading import Thread
from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.times import Timer
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from enconnect.fixtures import IRCClientSocket

from ..plugin import AutoNickPlugin
from ....clients.irc.test import IRCEVENTS

if TYPE_CHECKING:
    from ....robie import RobieService



IRCEVENTS = deepcopy(IRCEVENTS)



def test_AutoNickPlugin(
    service: 'RobieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    """

    plugin = (
        service.plugins
        .childs['autonick'])

    assert isinstance(
        plugin, AutoNickPlugin)


    attrs = lattrs(plugin)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params',
        '_AutoNickPlugin__started',
        '_AutoNickPlugin__nickserv',
        '_AutoNickPlugin__timer',
        '_RobiePlugin__thread']


    assert inrepr(
        'plugin.AutoNickPlugin',
        plugin)

    assert isinstance(
        hash(plugin), int)

    assert instr(
        'plugin.AutoNickPlugin',
        plugin)


    plugin.validate()

    assert plugin.robie

    assert plugin.enable

    assert plugin.name == 'autonick'

    assert plugin.kind == 'plugin'

    assert plugin.schema()

    assert plugin.params

    assert plugin.thread

    assert plugin.dumped



def test_AutoNickPlugin_cover(
    service: 'RobieService',
    client_ircsock: IRCClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    :param client_ircsock: Object to mock client connection.
    """

    plugin = (
        service.plugins
        .childs['autonick'])

    setattr(
        plugin,
        '_AutoNickPlugin__timer',
        Timer(0))


    client_ircsock([

        (':mocked 376 ircbot '
         ':End of /MOTD command.'),

        (':NickServ!a@b.c NOTICE '
         ' ircbot :This nickname'
         ' is registered.')])


    service.limit(
        plugins=[
            'autonick',
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
