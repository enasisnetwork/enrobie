"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

if TYPE_CHECKING:
    from ...service import RobieService



def test_RobiePlugins(
    service: 'RobieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    """

    member = service.plugins


    attrs = lattrs(member)

    assert attrs == [
        '_RobieMember__service',
        '_RobieMember__threads',
        '_RobieMember__mqueue',
        '_RobieMember__cqueue',
        '_RobieMember__vacate',
        '_RobieMember__cancel']


    assert inrepr(
        'plugins.RobiePlugins',
        member)

    assert isinstance(
        hash(member), int)

    assert instr(
        'plugins.RobiePlugins',
        member)


    assert member.robie

    assert member.service

    assert len(member.threads) == 7

    assert len(member.childs) == 7

    assert member.mqueue

    assert member.cqueue

    assert member.vacate

    assert member.cancel

    assert len(member.running) == 0


    member.operate()



def test_RobiePlugins_cover(
    service: 'RobieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    """

    member = service.plugins
    childs = member.childs

    assert all(
        x.thread
        for x in
        childs.values())
