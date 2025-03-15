"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inlist
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from ..plugin import RobiePluginThread

if TYPE_CHECKING:
    from ...service import RobieService



def test_RobiePluginThread(
    service: 'RobieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    """

    member = service.plugins

    threads = (
        member.threads
        .values())


    for thread in threads:

        assert isinstance(
            thread,
            RobiePluginThread)


        attrs = lattrs(thread)

        # Inherits Thread class

        assert inlist(
            '_RobieThread__member',
            attrs)

        assert inlist(
            '_RobieThread__child',
            attrs)

        assert inlist(
            '_RobieThread__mqueue',
            attrs)

        assert inlist(
            '_RobieThread__cqueue',
            attrs)


        assert inrepr(
            'Thread(RobiePlugin',
            thread)

        assert isinstance(
            hash(thread), int)

        assert instr(
            'Thread(RobiePlugin',
            thread)


        assert thread.robie

        assert thread.service

        assert thread.member

        assert thread.child

        assert thread.plugin

        assert thread.mqueue

        assert thread.cqueue

        assert not thread.congest

        assert not thread.enqueue
