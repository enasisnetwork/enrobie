"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import dumps
from typing import Optional
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
_NORESPOND = 'no_response'



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



def promptllm(  # noqa: CFQ001,CFQ002
    plugin: 'AinswerPlugin',
    client: 'RobieClient',
    prompt: str,
    *,
    whoami: str,
    author: str,
    anchor: str,
    message: str,
    header: Optional[str] = None,
    footer: Optional[str] = None,
    ignore: Optional[list[str]] = None,
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
    :param header: Optinoal header included before question.
    :param footer: Optinoal footer included after question.
    :param ignore: Optional reasons for LLM not responding.
    :returns: Message prefixed with runtime prompt values.
    """

    robie = plugin.robie
    history = plugin.history


    parsed = robie.j2parse(
        {'prompt': prompt,
         'header': header,
         'footer': footer},
        {'plugin': plugin,
         'client': client,
         'whoami': whoami,
         'author': author,
         'anchor': anchor,
         'message': message})

    prompt = parsed['prompt']
    header = parsed['header']
    footer = parsed['footer']

    assert isinstance(prompt, str)


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

        _items = '\n'.join([
            dumps(x)
            for x in items])

        return (
            ('**Conversations**'
             '\nYou have previously had'
             ' these conversations with'
             f' the user.\n{_items}\n\n')
            if items else SEMPTY)


    returned = (
        '**Instructions**'
        f'\n{prompt}\n\n'
        f'{_histories()}')


    if ignore is not None:

        ignored = (
            '\n - '
            .join(ignore))

        returned += (
            '**Not Responding**'
            '\nThere are reasons for'
            ' not responding to the'
            ' question. If you think'
            ' you should not respond'
            ' to the question, reply'
            f' with only {_NORESPOND}.'
            f'\nReasons for replying'
            f' with {_NORESPOND} are:'
            f'\n - {ignored}\n\n')


    returned += (
        '**User Information**'
        "\nThe user's nick"
        f' is {author}.\n\n')


    if header is not None:
        returned += (
            f'{header}\n\n')

    returned += (
        '**User Question**'
        f'\n{message}')

    if footer is not None:
        returned += (
            f'\n\n{footer}\n\n')


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


    assert mitem.whome
    assert mitem.author
    assert mitem.anchor
    assert mitem.message

    whoami = mitem.whome[0]
    author = mitem.author[0]
    anchor = mitem.anchor
    message = mitem.message


    client = (
        childs.clients
        [mitem.client])

    assert isinstance(
        client, DSCClient)


    if (mitem.kind == 'chanmsg'
            and not mitem.hasme):
        return None


    respond = AinswerResponseDSC

    ainswer = (
        plugin.ainswer(
            client,
            (params.prompt
             .client.dsc),
            whoami=whoami,
            author=author,
            anchor=anchor,
            message=message,
            respond=respond))


    if ainswer == _NORESPOND:
        return NCNone


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


    assert mitem.whome
    assert mitem.author
    assert mitem.anchor
    assert mitem.message

    whoami = mitem.whome[0]
    author = mitem.author[0]
    anchor = mitem.anchor
    message = mitem.message


    client = (
        childs.clients
        [mitem.client])

    assert isinstance(
        client, IRCClient)


    if (mitem.kind == 'chanmsg'
            and not mitem.hasme):
        return None


    respond = AinswerResponseIRC

    ainswer = (
        plugin.ainswer(
            client,
            (params.prompt
             .client.irc),
            whoami=whoami,
            author=author,
            anchor=anchor,
            message=message,
            respond=respond))


    if ainswer == _NORESPOND:
        return NCNone


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


    assert mitem.whome
    assert mitem.author
    assert mitem.anchor
    assert mitem.message

    whoami = mitem.whome[0]
    author = mitem.author[0]
    anchor = mitem.anchor
    message = mitem.message


    client = (
        childs.clients
        [mitem.client])

    assert isinstance(
        client, MTMClient)


    if (mitem.kind == 'chanmsg'
            and not mitem.hasme):
        return None


    respond = AinswerResponseMTM

    ainswer = (
        plugin.ainswer(
            client,
            (params.prompt
             .client.mtm),
            whoami=whoami,
            author=author,
            anchor=anchor,
            message=message,
            respond=respond))


    if ainswer == _NORESPOND:
        return NCNone


    citem = mitem.reply(
        robie, ainswer)

    cqueue.put(citem)
