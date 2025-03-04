"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import dumps
from typing import TYPE_CHECKING

from encommon.times import Time
from encommon.types import DictStrAny
from encommon.types.strings import SEMPTY

if TYPE_CHECKING:
    from .plugin import AinswerPlugin
    from ...robie.childs import RobieClient



def promptllm(  # noqa: CFQ002
    plugin: 'AinswerPlugin',
    client: 'RobieClient',
    prompt: str,
    *,
    whoami: str,
    author: str,
    anchor: str,
    message: str,
) -> str:
    """
    Return the message prefixed with runtime prompt values.

    :param plugin: Plugin class instance for Chatting Robie.
    :param client: Client class instance for Chatting Robie.
    :param prompt: Additional prompt insert before question.
    :param whoami: What is my current nickname on platform.
    :param author: Name of the user that submitted question.
    :param anchor: Channel name or other context or thread.
    :param message: Question that will be asked of the LLM.
    :returns: Message prefixed with runtime prompt values.
    """

    robie = plugin.robie
    history = plugin.history


    prompt = robie.j2parse(
        prompt,
        {'whoami': whoami,
         'plugin': plugin,
         'client': client})

    if not isinstance(prompt, str):
        raise ValueError('prompt')


    def _histories() -> str:

        items: list[DictStrAny] = []

        records = (
            history.records(
                client, anchor))

        for record in records:

            _author = record.author
            _message = record.message
            _ainswer = record.ainswer

            _create = (
                Time(record.create)
                .simple)

            items.extend([

                {'role': 'user',
                 'content': _message,
                 'nick': _author,
                 'time': _create},

                {'role': 'assistant',
                 'content': _ainswer,
                 'time': _create}])

        return (
            ('**Conversations**\n'
             f'{dumps(items)}\n\n')
            if items else SEMPTY)


    returned = (
        '**Instructions**'
        f'\n{prompt}\n\n'
        "The user's nickname"
        f' is {author}.\n\n'
        f'{_histories()}'
        '**User Question**'
        f'\n{message}')

    return returned.strip()
