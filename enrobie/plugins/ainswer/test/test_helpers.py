"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import loads
from typing import TYPE_CHECKING

from pydantic_ai.models.test import TestModel

from .test_history import _insert_history
from ..helpers import engagellm
from ..helpers import promptllm
from ..models import AinswerResponse
from ..plugin import AinswerPlugin

if TYPE_CHECKING:
    from ....robie import Robie



def test_engagellm(
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


    testing = TestModel()

    override_agent = (
        plugin.agent
        .override(
            model=testing))

    with override_agent:

        response = engagellm(
            plugin, 'Hello',
            AinswerResponse)

    assert response.text == 'a'



def test_promptllm(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients
    plugins = childs.plugins

    client = clients['ircbot']
    plugin = plugins['ainswer']

    assert isinstance(
        plugin, AinswerPlugin)

    _insert_history(
        plugin, client)


    message = 'This is the question'

    prompt = promptllm(
        plugin, client,
        (plugin.params
         .prompt.client.irc),
        whoami='Robie',
        author='nickname1',
        anchor='#channel',
        message=message,
        header='header',
        footer='footer')


    assert prompt.startswith(
        '**Instructions**\n'
        'Your nickname is'
        ' Robie. Keep it short'
        ' and use colors.\n\n'
        '**Conversations**\n')


    _, history = (
        prompt
        .split('**Conversations**\n'))

    _history = (
        history
        .split('\n', 22))


    records = [
        loads(x) for x
        in _history[1:-2]]

    assert len(records) == 20


    assert records[0] == {
        'content': 'Message 2',
        'nick': 'nickname3',
        'role': 'user',
        'time': records[0]['time']}

    assert records[1] == {
        'content': 'Ainswer 2',
        'role': 'assistant',
        'time': records[1]['time']}

    assert records[-2] == {
        'content': 'Message 4',
        'nick': 'nickname4',
        'role': 'user',
        'time': records[-2]['time']}

    assert records[-1] == {
        'content': 'Ainswer 4',
        'role': 'assistant',
        'time': records[-1]['time']}


    assert prompt.endswith(
        '**User Information**'
        "\nThe user's nick"
        ' is nickname1.\n\n'
        'header\n\n'
        '**User Question**\n'
        'This is the question'
        '\n\nfooter')
