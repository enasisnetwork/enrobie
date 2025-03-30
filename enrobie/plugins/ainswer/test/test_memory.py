"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from ..plugin import AinswerPlugin

if TYPE_CHECKING:
    from ....robie import Robie



def _ainswer_memory(
    plugin: AinswerPlugin,
) -> None:
    """
    Insert testing records into the provided memory object.

    :param plugin: Plugin class instance for Chatting Robie.
    """

    memory = plugin.memory


    for count in range(12):

        count += 1

        memory.insert(
            person='hubert',
            message=str(count))



def test_AinswerMemory(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    plugins = childs.plugins

    plugin = plugins['ainswer']

    assert isinstance(
        plugin, AinswerPlugin)


    memory = plugin.memory


    attrs = lattrs(memory)

    assert attrs == [
        '_AinswerMemory__plugin',
        '_AinswerMemory__connect',
        '_AinswerMemory__locker',
        '_AinswerMemory__sengine',
        '_AinswerMemory__session']


    assert inrepr(
        'memory.AinswerMemory',
        memory)

    assert isinstance(
        hash(memory), int)

    assert instr(
        'memory.AinswerMemory',
        memory)



def test_AinswerMemory_cover(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    plugins = childs.plugins

    plugin = plugins['ainswer']

    assert isinstance(
        plugin, AinswerPlugin)


    memory = plugin.memory


    _ainswer_memory(plugin)


    records = (
        memory.search(
            person='hubert'))

    assert len(records) == 10


    record = (
        records[0].endumped)

    assert record == {
        'create': record['create'],
        'message': '3',
        'person': 'hubert',
        'plugin': 'ainswer',
        'unique': record['unique']}


    unique = records[0].unique

    memory.delete(
        'hubert', unique)


    records = (
        memory.search(
            person='hubert'))

    assert len(records) == 9
