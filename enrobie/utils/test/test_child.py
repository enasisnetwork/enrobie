"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from ..child import InvalidChild

if TYPE_CHECKING:
    from ...robie import Robie



def test_InvalidChild() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    raises = InvalidChild(
        child='invalid',
        phase='initial')


    attrs = lattrs(raises)

    assert attrs == [
        'child',
        'about']


    assert inrepr(
        'InvalidChild',
        raises)

    assert isinstance(
        hash(raises), int)

    assert instr(
        'Child (invalid)',
        raises)


    assert str(raises) == (
        'Child (invalid) '
        'invalid within '
        'phase (initial)')



def test_InvalidChild_cover(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    client = clients['ircbot']


    raises = InvalidChild(
        child=client,
        phase='runtime',
        about='about')

    name = client.name

    assert str(raises) == (
        f'Child ({name}) '
        'invalid within phase '
        '(runtime) (about)')
