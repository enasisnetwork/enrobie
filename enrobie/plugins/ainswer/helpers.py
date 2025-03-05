"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import dumps
from re import IGNORECASE
from re import match as re_match
from re import search as re_search
from typing import TYPE_CHECKING
from typing import Type

from encommon.times import Time
from encommon.types import DictStrAny
from encommon.types import NCNone
from encommon.types.strings import SEMPTY

from enconnect.discord import (
    ClientEvent as DSCClientEvent)
from enconnect.irc import (
    ClientEvent as IRCClientEvent)
from enconnect.mattermost import (
    ClientEvent as MTMClientEvent)

from .models import AinswerResponse
from .models import AinswerResponseDSC
from .models import AinswerResponseIRC
from .models import AinswerResponseMTM

if TYPE_CHECKING:
    from .plugin import AinswerPlugin
    from ...robie.childs import RobieClient
    from ...robie.models import RobieCommand
    from ...robie.models import RobieMessage
    from ...robie.addons import RobieQueue



_KINDS = ['privmsg', 'chanmsg']



def engagellm(
    plugin: 'AinswerPlugin',
    message: str,
    respond: Type[AinswerResponse],
) -> AinswerResponse:
    """
    Submit the question to the LLM and return the response.

    :param plugin: Plugin class instance for Chatting Robie.
    :param message: Question that will be asked of the LLM.
    :param respond: Model to describe the expected response.
    :returns: Response adhering to provided specifications.
    """

    agent = plugin.agent
    request = agent.run_sync

    runsync = request(
        user_prompt=message,
        result_type=respond)

    return runsync.data



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
        f'{_histories()}'
        '**User Information**'
        "\nThe user's nick"
        f' is {author}.\n\n'
        '**User Question**'
        f'\n{message}')

    return returned.strip()



def composedsc(
    plugin: 'AinswerPlugin',
    cqueue: 'RobieQueue[RobieCommand]',
    mitem: 'RobieMessage',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param cqueue: Queue instance where the item is received.
    :param mitem: Item containing information for operation.
    """

    from ...clients import DSCClient

    robie = plugin.robie
    childs = robie.childs
    params = plugin.params


    kind = mitem.kind

    if kind not in _KINDS:
        return NCNone


    event = getattr(
        mitem, 'event')

    assert isinstance(
        event,
        DSCClientEvent)


    assert event.message
    assert event.author
    assert event.recipient

    author = event.author[0]
    message = event.message


    client = (
        childs.clients
        [mitem.client])

    assert isinstance(
        client, DSCClient)

    current = (
        client.client
        .nickname)

    assert current is not None

    _current = current[0]


    ignore = _nocompose(
        _current, message)

    if (mitem.kind == 'chanmsg'
            and ignore is True):
        return None


    respond = AinswerResponseDSC

    anchor = (
        event.recipient[1]
        if kind == 'chanmsg'
        else event.author[1])

    ainswer = (
        plugin.ainswer(
            client,
            (params.prompt
             .client.dsc),
            whoami=_current,
            author=author,
            anchor=anchor,
            message=message,
            respond=respond))


    citem = mitem.reply(
        robie, ainswer)

    cqueue.put(citem)



def composeirc(
    plugin: 'AinswerPlugin',
    cqueue: 'RobieQueue[RobieCommand]',
    mitem: 'RobieMessage',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param cqueue: Queue instance where the item is received.
    :param mitem: Item containing information for operation.
    """

    from ...clients import IRCClient

    robie = plugin.robie
    childs = robie.childs
    params = plugin.params


    kind = mitem.kind

    if kind not in _KINDS:
        return NCNone


    event = getattr(
        mitem, 'event')

    assert isinstance(
        event,
        IRCClientEvent)


    assert event.message
    assert event.author
    assert event.recipient

    author = event.author
    message = event.message


    client = (
        childs.clients
        [mitem.client])

    assert isinstance(
        client, IRCClient)

    current = (
        client.client
        .nickname)

    assert current is not None


    ignore = _nocompose(
        current, message)

    if (mitem.kind == 'chanmsg'
            and ignore is True):
        return None


    respond = AinswerResponseIRC

    anchor = (
        event.recipient
        if kind == 'chanmsg'
        else event.author)

    ainswer = (
        plugin.ainswer(
            client,
            (params.prompt
             .client.irc),
            whoami=current,
            author=author,
            anchor=anchor,
            message=message,
            respond=respond))


    citem = mitem.reply(
        robie, ainswer)

    cqueue.put(citem)



def composemtm(
    plugin: 'AinswerPlugin',
    cqueue: 'RobieQueue[RobieCommand]',
    mitem: 'RobieMessage',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param cqueue: Queue instance where the item is received.
    :param mitem: Item containing information for operation.
    """

    from ...clients import MTMClient

    robie = plugin.robie
    childs = robie.childs
    params = plugin.params


    kind = mitem.kind

    if kind not in _KINDS:
        return NCNone


    event = getattr(
        mitem, 'event')

    assert isinstance(
        event,
        MTMClientEvent)


    assert event.message
    assert event.author
    assert event.recipient

    author = event.author[0][1:]
    message = event.message


    client = (
        childs.clients
        [mitem.client])

    assert isinstance(
        client, MTMClient)

    current = (
        client.client
        .nickname)

    assert current is not None

    _current = current[0][1:]


    ignore = _nocompose(
        _current, message)

    if (mitem.kind == 'chanmsg'
            and ignore is True):
        return None


    respond = AinswerResponseMTM

    anchor = (
        event.recipient[1]
        if kind == 'chanmsg'
        else event.author[1])

    ainswer = (
        plugin.ainswer(
            client,
            (params.prompt
             .client.mtm),
            whoami=_current,
            author=author,
            anchor=anchor,
            message=message,
            respond=respond))


    citem = mitem.reply(
        robie, ainswer)

    cqueue.put(citem)



def _nocompose(
    current: str,
    question: str,
) -> bool:
    """
    Return the boolean indicating that we are not reference.

    :param current: Current nickname of the operated client.
    :param question: Question that will be asked of the LLM.
    :returns: Boolean indicating that we are not reference.
    """

    return not any([

        re_search(
            (rf'\s{current}'
             r'(\;|\,|\-|\s|$)'),
            question,
            IGNORECASE),

        re_match(
            (r'^(\s+)?\@?'
             f'{current}'
             r'(\:|\,|\-)?\s+'),
            question,
            IGNORECASE)])
