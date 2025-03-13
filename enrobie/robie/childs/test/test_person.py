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



def test_RobieClient_cover(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    persons = childs.persons
    clients = childs.clients

    client = clients['ircbot']


    person = persons['hubert']


    attrs = lattrs(person)

    assert attrs == [
        '_RobieChild__robie',
        '_RobieChild__name',
        '_RobieChild__params']


    assert inrepr(
        'person.RobiePerson',
        person)

    assert isinstance(
        hash(person), int)

    assert instr(
        'person.RobiePerson',
        person)


    person.validate()

    assert person.robie

    assert person.enable

    assert person.name == 'hubert'

    assert person.kind == 'person'

    assert person.params

    assert person.dumped

    assert person.first == 'Hubert'

    assert person.last == 'Farnsworth'

    assert person.about

    assert person.weight


    assert not person.match(
        client, 'anonymous')

    assert person.match(
        client,
        'hubert!hubert@science.com')

    assert not person.match(
        client,
        'bender!bender@bending.com')
