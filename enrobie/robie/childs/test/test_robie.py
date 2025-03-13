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
    from ...robie import Robie



def test_RobieChilds(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs


    attrs = lattrs(childs)

    assert attrs == [
        '_RobieChilds__robie',
        '_RobieChilds__clients',
        '_RobieChilds__plugins',
        '_RobieChilds__persons']


    assert inrepr(
        'robie.RobieChilds',
        childs)

    assert isinstance(
        hash(childs), int)

    assert instr(
        'robie.RobieChilds',
        childs)


    childs.validate()

    assert childs.clients

    assert childs.plugins

    assert childs.persons
