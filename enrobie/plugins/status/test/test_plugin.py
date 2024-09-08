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

from enconnect.fixtures import DSCClientSocket
from enconnect.fixtures import IRCClientSocket
from enconnect.fixtures import MTMClientSocket

from ..plugin import StatusPlugin

if TYPE_CHECKING:
    from ....robie import Robie
    from ....robie import RobieService



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

IRCEVENTS = [
    (':n!u@h PRIVMSG '
     '#chan :!status')]

MTMEVENTS = [
    {'event': 'posted',
     'seq': 5,
     'broadcast': {
         'channel_id': 'nwyxekd4k7'},
     'data': {
         'channel_type': 'P',
         'post': (
             '{"user_id":"ietyrmdt5b",'
             '"channel_id":"nwyxekd4k7",'
             '"message":"!status"}'),
         'sender_name': '@robert'}}]



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

    service.start()


    thread = Thread(
        target=service.operate)

    thread.start()


    block_sleep(10)

    service.soft()

    while service.running:
        block_sleep(1)

    service.stop()

    thread.join()

    assert not service.congest
