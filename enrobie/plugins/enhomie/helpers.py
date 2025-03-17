"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...robie.models import RobieMessage
    from .plugin import HomiePlugin



def composedsc(
    plugin: 'HomiePlugin',
    mitem: 'RobieMessage',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param mitem: Item containing information for operation.
    :param status: Object containing the status information.
    """

    from ...clients.discord.message import DSCMessage


    assert plugin.thread

    thread = plugin.thread
    robie = plugin.robie
    member = thread.member
    cqueue = member.cqueue
    persist = plugin.persist

    assert isinstance(
        mitem, DSCMessage)

    assert mitem.message

    unique = (
        mitem.message
        .split(' ', 1)[1])

    current = (
        persist
        .record(unique))

    citem = mitem.reply(
        robie, str(current))

    cqueue.put(citem)



def composeirc(
    plugin: 'HomiePlugin',
    mitem: 'RobieMessage',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param mitem: Item containing information for operation.
    :param status: Object containing the status information.
    """

    from ...clients.irc.message import IRCMessage


    assert plugin.thread

    thread = plugin.thread
    robie = plugin.robie
    member = thread.member
    cqueue = member.cqueue
    persist = plugin.persist

    assert isinstance(
        mitem, IRCMessage)

    assert mitem.message

    unique = (
        mitem.message
        .split(' ', 1)[1])

    current = (
        persist
        .record(unique))

    citem = mitem.reply(
        robie, str(current))

    cqueue.put(citem)



def composemtm(
    plugin: 'HomiePlugin',
    mitem: 'RobieMessage',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param mitem: Item containing information for operation.
    :param status: Object containing the status information.
    """

    from ...clients.mattermost.message import MTMMessage


    assert plugin.thread

    thread = plugin.thread
    robie = plugin.robie
    member = thread.member
    cqueue = member.cqueue
    persist = plugin.persist

    assert isinstance(
        mitem, MTMMessage)

    assert mitem.message

    unique = (
        mitem.message
        .split(' ', 1)[1])

    current = (
        persist
        .record(unique))

    citem = mitem.reply(
        robie, str(current))

    cqueue.put(citem)
