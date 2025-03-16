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



def test_RobiePerson(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    persons = childs.persons
    clients = childs.clients


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


    assert person.match(
        clients['dscbot'],
        '823039201390230492')

    assert not person.match(
        clients['dscbot'],
        '823902304920392013')


    assert not person.match(
        clients['ircbot'],
        'anonymous')

    assert person.match(
        clients['ircbot'],
        'hubert!hubert@science.com')

    assert not person.match(
        clients['ircbot'],
        'bender!bender@bending.com')


    assert person.match(
        clients['mtmbot'],
        'kjf9al2klaiietalkw')

    assert not person.match(
        clients['mtmbot'],
        'iietalkwkjf9al2kla')
