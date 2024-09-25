"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from ..param import InvalidParam

if TYPE_CHECKING:
    from ...robie import Robie



def test_InvalidParam(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    client = clients['ircbot']


    raises = InvalidParam(
        error='invalid',
        about='about',
        child=client,
        param='param',
        value='value')


    attrs = lattrs(raises)

    assert attrs == [
        'error',
        'about',
        'child',
        'param',
        'value']


    assert inrepr(
        'InvalidParam',
        raises)

    assert isinstance(
        hash(raises), int)

    assert instr(
        'Error (invalid)',
        raises)


    assert str(raises) == (
        'Error (invalid) '
        'param (param) '
        'value (value) child '
        '(IRCClient/ircbot)'
        ' (about)')
