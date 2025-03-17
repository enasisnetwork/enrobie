"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...robie.models import RobieMessage
    from .plugin import NagiosPlugin



def composedsc(
    plugin: 'NagiosPlugin',
    mitem: 'RobieMessage',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param mitem: Item containing information for operation.
    :param status: Object containing the status information.
    """

    assert plugin.thread

    thread = plugin.thread
    robie = plugin.robie
    member = thread.member
    cqueue = member.cqueue
    current = plugin.current

    summary = current.summary

    citem = mitem.reply(
        robie, str(summary))

    cqueue.put(citem)



def composeirc(
    plugin: 'NagiosPlugin',
    mitem: 'RobieMessage',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param mitem: Item containing information for operation.
    :param status: Object containing the status information.
    """

    assert plugin.thread

    thread = plugin.thread
    robie = plugin.robie
    member = thread.member
    cqueue = member.cqueue
    current = plugin.current

    summary = current.summary

    citem = mitem.reply(
        robie, str(summary))

    cqueue.put(citem)



def composemtm(
    plugin: 'NagiosPlugin',
    mitem: 'RobieMessage',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param mitem: Item containing information for operation.
    :param status: Object containing the status information.
    """

    assert plugin.thread

    thread = plugin.thread
    robie = plugin.robie
    member = thread.member
    cqueue = member.cqueue
    current = plugin.current

    summary = current.summary

    citem = mitem.reply(
        robie, str(summary))

    cqueue.put(citem)
