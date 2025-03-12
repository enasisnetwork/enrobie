"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from pydantic_ai.models.test import TestModel

from ..models import AinswerResponse
from ..plugin import AinswerPlugin

if TYPE_CHECKING:
    from ....robie import Robie



def test_AinswerQuestion_engage(
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

    question = plugin.question


    testing = TestModel()

    override_agent = (
        plugin.agent
        .override(
            model=testing))

    with override_agent:

        response = (
            question.submit(
                'Hello World!',
                AinswerResponse))

    assert response.text == 'a'



def test_AinswerQuestion_prompt(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """
