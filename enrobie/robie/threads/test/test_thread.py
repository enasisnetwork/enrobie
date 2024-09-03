"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.times import Time

from ...childs import RobieClient
from ...models import RobieCommand
from ...models import RobieMessage

if TYPE_CHECKING:
    from ...service import RobieService



def test_RobieThread_cover(
    service: 'RobieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    """

    member = service.clients

    message = RobieMessage
    command = RobieCommand


    threads = (
        member.threads
        .values())

    for thread in threads:

        child = thread.child

        assert isinstance(
            child, RobieClient)


        mitem = message(child)

        expired = (
            thread.expired(mitem))

        assert expired is False

        mitem.time = Time('-1h')

        expired = (
            thread.expired(mitem))

        assert expired is True


        citem = command(child)

        expired = (
            thread.expired(citem))

        assert expired is False

        citem.time = Time('-1h')

        expired = (
            thread.expired(citem))

        assert expired is True
