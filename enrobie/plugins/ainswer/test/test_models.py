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
    from ....robie import RobieService



def test_AinswerModels(
    service: 'RobieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Chatting Robie class instance.
    """

    plugin = (
        service.plugins
        .childs['ainswer'])

    assert isinstance(
        plugin, AinswerPlugin)


    models = plugin.models


    attrs = lattrs(models)

    assert attrs == [
        '_AinswerModels__plugin']


    assert inrepr(
        'models.AinswerModels',
        models)

    assert isinstance(
        hash(models), int)

    assert instr(
        'models.AinswerModels',
        models)


    assert models.agent()

    assert models.settings()

    assert models.anthropic

    assert models.openai
