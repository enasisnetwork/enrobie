"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from threading import Thread
from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from enconnect.fixtures import IRCClientSocket
from enconnect.irc.test import EVENTS as IRCEVENTS

from ..plugin import AutoJoinPlugin

if TYPE_CHECKING:
    from ....robie import Robie
    from ....robie import RobieService



IRCEVENTS = deepcopy(IRCEVENTS)



def test_AutoJoinPlugin(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    plugins = childs.plugins


    plugin = plugins['autojoin']

    assert isinstance(
        plugin, AutoJoinPlugin)


    attrs = lattrs(plugin)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params',
        '_AutoJoinPlugin__joined',
        '_AutoJoinPlugin__should',
        '_AutoJoinPlugin__timer']


    assert inrepr(
        'plugin.AutoJoinPlugin',
        plugin)

    assert isinstance(
        hash(plugin), int)

    assert instr(
        'plugin.AutoJoinPlugin',
        plugin)


    plugin.validate()

    assert plugin.robie

    assert plugin.enable

    assert plugin.name == 'autojoin'

    assert plugin.kind == 'plugin'

    assert plugin.schema()

    assert plugin.params

    assert plugin.dumped



def test_AutoJoinPlugin_cover(
    service: 'RobieService',
    client_ircsock: IRCClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    :param client_ircsock: Object to mock client connection.
    """

    events = [

        (':mocked 376 ircbot '
         ':End of /MOTD command.'),

        ':ircbot JOIN :#test',

        (':foo!bar@baz KICK '
         '#test ircbot :foo'),

        ':ircbot JOIN :#test',

        ':ircbot PART :#test',

        ('ERROR :Closing Link: ircbot'
         '[mocked] (Quit: ircbot)')]


    client_ircsock(events)

    service.limit_threads(
        clients=['ircbot'],
        plugins=['autojoin'])

    service.start()


    thread = Thread(
        target=service.operate)

    thread.start()


    block_sleep(6)

    service.soft()

    while service.running:
        block_sleep(1)

    service.stop()

    thread.join()
