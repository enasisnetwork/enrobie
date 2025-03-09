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
from encommon.types.strings import COMMAS
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



def promptllm(  # noqa: CFQ001,CFQ002,CFQ004
    plugin: 'AinswerPlugin',
    client: 'RobieClient',
    prompt: str,
    *,
    whoami: str,
    author: str,
    anchor: str,
    message: str,
    whoami_uniq: Optional[str] = None,
    author_uniq: Optional[str] = None,
    header: Optional[str] = None,
    footer: Optional[str] = None,
    ignore: Optional[list[str]] = None,
    mitem: Optional['RobieMessage'] = None,
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
    :param mitem: Item containing information for operation.
    :returns: Message prefixed with runtime prompt values.
    """

    robie = plugin.robie
    history = plugin.history
    family = client.family
    noresp = _NORESPOND


    parsed = robie.j2parse(
        {'prompt': prompt,
         'header': header,
         'footer': footer},
        {'plugin': plugin,
         'client': client,
         'family': family,
         'whoami': whoami,
         'whoami_uniq': whoami_uniq,
         'author': author,
         'author_uniq': author_uniq,
         'anchor': anchor,
         'message': message,
         'mitem': mitem})

    prompt = parsed['prompt']
    header = parsed['header']
    footer = parsed['footer']

    assert isinstance(prompt, str)


    def _history() -> str:

        if anchor is None:
            return SEMPTY  # NOCVR

        items: list[DictStrAny] = []

        records = (
            history.records(
                client, anchor))

        for record in records:

            author = record.author
            message = record.message
            ainswer = record.ainswer

            create = (
                Time(record.create)
                .simple)

            items.extend([
                {'role': 'user',
                 'content': message,
                 'nick': author,
                 'time': create},
                {'role': 'assistant',
                 'content': ainswer,
                 'time': create}])

        joined = '\n'.join([
            dumps(x)
            for x in items])

        return (
            ('**Previous**\n'
             'You have previously'
             ' had the following'
             ' conversations in the'
             ' channel with users.'
             f'\n{joined}\n\n')
            if items else SEMPTY)


    def _ignored() -> str:

        if ignore is None:
            return SEMPTY

        joined = (
            '\n - '.join(ignore))

        return (
            '**Responding**\n'
            'There are reasons for'
            ' not responding to the'
            ' user question. If you'
            ' think you should not'
            ' respond, simply reply'
            f' with only {noresp}.\n'
            f'Reasons for replying'
            f' {noresp} include:'
            f'\n - {joined}\n\n')


    def _metadata() -> str:

        returned = (
            '**Message**\n'
            'Your nickname:'
            f' {whoami}\n')

        if whoami_uniq is not None:
            returned += (
                'Your ID: '
                f'{whoami_uniq}\n')

        returned += (
            'User nickname:'
            f' {author}\n')

        if author_uniq is not None:
            returned += (
                'User ID: '
                f'{author_uniq}\n')

        returned += (
            'Client family:'
            f' {family}\n')

        if mitem is not None:

            kind = mitem.kind
            time = mitem.time

            returned += (
                f'Time: {time}\n'
                f'Kind: {kind}\n')

        return returned


    def _channel() -> str:

        channel = (
            client.channels
            .select(anchor))

        if channel is None:
            return SEMPTY

        title = channel.title
        topic = channel.topic

        returned = (
            f'Unique: {anchor}\n')

        if (title is not None
                and title != anchor):
            returned += (
                f'Title: {title}\n')

        if topic is not None:
            returned += (
                f'Topic: {topic}\n')

        if channel.members:

            join = COMMAS.join(
                channel.members)

            returned += (
                f'Users: {join}\n')

        return (
            '\n**Channel**\n'
            f'{returned}')


    returned = SEMPTY.join([
        ('**Instructions**\n'
         f'{prompt}\n\n'
         f'{_history()}'
         f'{_ignored()}'
         f'{_metadata()}'
         f'{_channel()}\n'),
        (f'{header}\n\n'
         if header is not None
         and len(header) >= 1
         else SEMPTY),
        ('**Question**\n'
         f'{message}\n\n'),
        (f'{footer}\n\n'
         if footer is not None
         and len(footer) >= 1
         else SEMPTY)])

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
    hasme = mitem.hasme


    if kind not in _KINDS:
        return NCNone

    if (kind == 'chanmsg'
            and not hasme):
        return None


    event = getattr(
        mitem, 'event')

    assert isinstance(
        event,
        DSCClientEvent)


    client = (
        childs.clients
        [mitem.client])

    assert isinstance(
        client, DSCClient)


    ainswer = (
        plugin.ainswer(
            client,
            (params.prompt
             .client.dsc),
            AinswerResponseDSC,
            mitem=mitem))


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
    hasme = mitem.hasme


    if kind not in _KINDS:
        return NCNone

    if (kind == 'chanmsg'
            and not hasme):
        return None


    event = getattr(
        mitem, 'event')

    assert isinstance(
        event,
        IRCClientEvent)


    client = (
        childs.clients
        [mitem.client])

    assert isinstance(
        client, IRCClient)


    ainswer = (
        plugin.ainswer(
            client,
            (params.prompt
             .client.irc),
            AinswerResponseIRC,
            mitem=mitem))


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
    hasme = mitem.hasme


    if kind not in _KINDS:
        return NCNone

    if (kind == 'chanmsg'
            and not hasme):
        return None


    event = getattr(
        mitem, 'event')

    assert isinstance(
        event,
        MTMClientEvent)


    client = (
        childs.clients
        [mitem.client])

    assert isinstance(
        client, MTMClient)


    ainswer = (
        plugin.ainswer(
            client,
            (params.prompt
             .client.mtm),
            AinswerResponseMTM,
            mitem=mitem))


    if ainswer == _NORESPOND:
        return NCNone


    citem = mitem.reply(
        robie, ainswer)

    cqueue.put(citem)
