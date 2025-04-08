"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from ...models import RobieModels

if TYPE_CHECKING:
    from ...robie import Robie



def test_RobiePlugin_cover(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients
    plugins = childs.plugins
    persons = childs.persons

    client = clients['ircbot']
    plugin = plugins['status']

    RobieMessage = (
        RobieModels
        .message())

    params = plugin.params

    mitem1 = RobieMessage(client)
    mitem2 = RobieMessage(client)

    mitem1.person = 'hubert'


    assert plugin.trusted(mitem1)
    assert plugin.trusted(mitem2)

    assert plugin.trusted(
        persons['hubert'])

    assert plugin.trusted(
        persons['bender'])

    params.trusted = ['hubert']


    assert plugin.trusted(mitem1)
    assert plugin.notrust(mitem2)

    assert plugin.trusted(
        persons['hubert'])

    assert plugin.notrust(
        persons['bender'])
