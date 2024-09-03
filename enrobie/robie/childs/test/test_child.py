"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...robie import Robie



def test_RobieChild_cover(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    child1 = clients['ircbot']
    child2 = clients['dscbot']


    sort = [child1, child2]

    assert sorted(sort) == [
        child2, child1]
