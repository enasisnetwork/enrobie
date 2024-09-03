"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread
from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from enconnect.fixtures import DSCClientSocket
from enconnect.fixtures import IRCClientSocket
from enconnect.fixtures import client_dscsock  # noqa: F401
from enconnect.fixtures import client_ircsock  # noqa: F401

from ..plugin import StatusPlugin

if TYPE_CHECKING:
    from ....robie import Robie
    from ....robie import RobieService



IRCEVENTS = [
    'PING :123456789',
    (':n!u@h PRIVMSG '
     '#chan :!status'),
    'PING :123456789',
    (':n!u@h PRIVMSG '
     '#chan :!status'),
    'PING :123456789',
    (':n!u@h PRIVMSG '
     '#chan :!status'),
    'PING :123456789']

DSCEVENTS = [
    {'t': 'MESSAGE_CREATE',
     's': 3,
     'op': 0,
     'd': {
         'id': '33330001',
         'channel_id': '22220001',
         'author': {
             'id': '44444444',
             'username': 'Author'},
         'content': '!status'}}]



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
        '_RobieChild__params']


    assert inrepr(
        'plugin.StatusPlugin',
        plugin)

    assert hash(plugin) > 0

    assert instr(
        'plugin.StatusPlugin',
        plugin)


    plugin.validate()

    assert plugin.robie

    assert plugin.name == 'status'

    assert plugin.kind == 'plugin'

    assert plugin.params

    assert plugin.dumped



def test_StatusPlugin_cover(
    service: 'RobieService',
    client_ircsock: IRCClientSocket,  # noqa: F811
    client_dscsock: DSCClientSocket,  # noqa: F811
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    :param client_ircsock: Object to mock client connection.
    :param client_dscsock: Object to mock client connection.
    """

    service.start()


    def _operate() -> None:

        client_ircsock(IRCEVENTS)
        client_dscsock(DSCEVENTS)

        service.operate()


    thread = Thread(
        target=_operate)

    thread.start()

    for _ in range(100):
        thread.join(0.1)

    service.soft()

    while service.enqueue:
        thread.join(0.1)  # NOCVR

    while service.running:
        thread.join(0.1)  # NOCVR

    service.stop()

    thread.join()

    assert not service.enqueue
