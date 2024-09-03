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
from enconnect.fixtures import client_dscsock  # noqa: F401
from enconnect.fixtures import client_ircsock  # noqa: F401

from ..models import RobieMessage

if TYPE_CHECKING:
    from ..service import RobieService



def test_RobieService(
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

    assert hash(service) > 0

    assert instr(
        'service.RobieService',
        service)


    assert service.robie

    assert service.params

    assert service.clients

    assert service.plugins

    assert len(service.running) == 0

    assert len(service.zombies) == 3


    service.start()


    def _operate() -> None:

        client_ircsock()
        client_dscsock()

        service.operate()


    thread = Thread(
        target=_operate)

    thread.start()

    block_sleep(10)

    assert service.running

    assert not service.zombies

    assert not service.congest

    service.soft()

    while service.enqueue:
        thread.join(0.1)  # NOCVR

    while service.running:
        thread.join(0.1)  # NOCVR

    service.stop()

    thread.join()

    assert service.zombies

    assert not service.congest

    assert not service.enqueue



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

    model = RobieMessage

    item = model(client)


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

    service.stop()
    service.soft()
    service.start()
    service.start()
    service.soft()
    service.soft()
    service.stop()
    service.stop()
