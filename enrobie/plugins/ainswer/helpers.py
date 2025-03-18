"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING
from typing import get_args

from encommon.types import NCNone

from .ainswer import AinswerIgnored
from .common import AinswerResponseDSC
from .common import AinswerResponseIRC
from .common import AinswerResponseMTM
from .history import AinswerHistoryKinds

if TYPE_CHECKING:
    from .plugin import AinswerPlugin
    from ...robie.models import RobieMessage



_KINDS = get_args(AinswerHistoryKinds)



def composedsc(  # noqa: CFQ004
    plugin: 'AinswerPlugin',
    mitem: 'RobieMessage',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param mitem: Item containing information for operation.
    """

    from ...clients import DSCClient
    from ...clients.discord.message import DSCMessage


    assert plugin.thread

    thread = plugin.thread
    robie = plugin.robie
    childs = robie.childs
    params = plugin.params
    member = thread.member
    cqueue = member.cqueue

    kind = mitem.kind
    hasme = mitem.hasme
    message = mitem.message


    if kind not in _KINDS:
        return NCNone

    if (kind == 'chanmsg'
            and not hasme):
        return None


    assert message is not None

    firschar = (
        message[0].strip())

    if firschar in '!%&/.':
        return NCNone


    assert isinstance(
        mitem, DSCMessage)

    type = mitem.event.type

    if type == 'MESSAGE_UPDATE':
        return NCNone


    client = (
        childs.clients
        [mitem.client])

    assert isinstance(
        client, DSCClient)


    prompt = (
        params.prompt
        .client.dsc)

    ainswer = (
        plugin.ainswer(
            mitem, prompt,
            AinswerResponseDSC))


    if ainswer == AinswerIgnored:
        return NCNone


    citem = mitem.reply(
        robie, ainswer)

    cqueue.put(citem)



def composeirc(  # noqa: CFQ004
    plugin: 'AinswerPlugin',
    mitem: 'RobieMessage',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param mitem: Item containing information for operation.
    """

    from ...clients import IRCClient


    assert plugin.thread

    thread = plugin.thread
    robie = plugin.robie
    childs = robie.childs
    params = plugin.params
    member = thread.member
    cqueue = member.cqueue

    kind = mitem.kind
    hasme = mitem.hasme
    message = mitem.message


    if kind not in _KINDS:
        return NCNone

    if (kind == 'chanmsg'
            and not hasme):
        return None


    assert message is not None

    firschar = (
        message[0].strip())

    if firschar in '!%&/.':
        return NCNone


    client = (
        childs.clients
        [mitem.client])

    assert isinstance(
        client, IRCClient)


    prompt = (
        params.prompt
        .client.irc)

    ainswer = (
        plugin.ainswer(
            mitem, prompt,
            AinswerResponseIRC))


    if ainswer == AinswerIgnored:
        return NCNone


    citem = mitem.reply(
        robie, ainswer)

    cqueue.put(citem)



def composemtm(  # noqa: CFQ004
    plugin: 'AinswerPlugin',
    mitem: 'RobieMessage',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param mitem: Item containing information for operation.
    """

    from ...clients import MTMClient
    from ...clients.mattermost.message import MTMMessage


    assert plugin.thread

    thread = plugin.thread
    robie = plugin.robie
    childs = robie.childs
    params = plugin.params
    member = thread.member
    cqueue = member.cqueue

    kind = mitem.kind
    hasme = mitem.hasme
    message = mitem.message


    if kind not in _KINDS:
        return NCNone

    if (kind == 'chanmsg'
            and not hasme):
        return None


    assert message is not None

    firschar = (
        message[0].strip())

    if firschar in '!%&/.':
        return NCNone


    assert isinstance(
        mitem, MTMMessage)

    type = mitem.event.type

    if type == 'post_edited':
        return NCNone


    client = (
        childs.clients
        [mitem.client])

    assert isinstance(
        client, MTMClient)


    prompt = (
        params.prompt
        .client.mtm)

    ainswer = (
        plugin.ainswer(
            mitem, prompt,
            AinswerResponseMTM))


    if ainswer == AinswerIgnored:
        return NCNone


    citem = mitem.reply(
        robie, ainswer)

    cqueue.put(citem)
