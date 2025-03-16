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

from ..models import RobieMessage

if TYPE_CHECKING:
    from ..service import RobieService



def test_RobieService(
    service: 'RobieService',
    client_dscsock: DSCClientSocket,
    client_ircsock: IRCClientSocket,
    client_mtmsock: MTMClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    :param client_ircsock: Object to mock client connection.
    :param client_dscsock: Object to mock client connection.
    :param client_mtmsock: Object to mock client connection.
    """


    attrs = lattrs(service)

    assert attrs == [
        '_RobieService__robie',
        '_RobieService__clients',
        '_RobieService__plugins',
        '_RobieService__timer',
        '_RobieService__vacate',
        '_RobieService__cancel',
        '_RobieService__started']


    assert inrepr(
        'service.RobieService',
        service)

    assert isinstance(
        hash(service), int)

    assert instr(
        'service.RobieService',
        service)


    assert service.robie

    assert service.params

    assert service.clients

    assert service.plugins

    assert len(service.running) == 0

    assert len(service.zombies) == 10


    client_dscsock()
    client_ircsock()
    client_mtmsock()

    service.limit(
        plugins=['status'])

    service.start()

    assert len(service.running) == 4


    thread = Thread(
        target=service.operate)

    thread.start()


    block_sleep(10)

    assert service.running

    assert not service.zombies

    service.soft()

    while service.running:
        block_sleep(1)

    service.stop()

    thread.join()

    assert service.zombies

    # Not testing congest

    assert service.enqueue



def test_RobieService_healths(
    service: 'RobieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    """

    robie = service.robie
    childs = robie.childs
    clients = childs.clients
    member = service.clients
    threads = member.threads

    client = clients['ircbot']
    thread = threads['ircbot']
    mqueue = thread.mqueue

    item = RobieMessage(client)


    for _ in range(6):
        mqueue.put(item)


    assert service.congest

    service.operate_healths()



def test_RobieService_cover(
    service: 'RobieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    """

    service.limit(
        clients=['ircbot'],
        plugins=['status'])

    service.stop()
    service.soft()
    service.start()
    service.start()
    service.soft()
    service.soft()
    service.stop()
    service.stop()
