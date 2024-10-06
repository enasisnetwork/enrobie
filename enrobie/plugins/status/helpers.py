"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from encommon.types import DictStrAny
from encommon.types import sort_dict

from .common import StatusPluginItem
from ...robie import Robie
from ...robie.addons import RobieQueue
from ...robie.models import RobieCommand
from ...robie.models import RobieMessage



def grouped(
    status: dict[str, StatusPluginItem],
) -> dict[str, list[StatusPluginItem]]:
    """
    Return the dictionary with status value stored by group.

    :param status: Object containing the status information.
    :returns: Dictionary with status value stored by group.
    """

    groups: DictStrAny = {
        x.group: [] for x
        in status.values()}

    items = status.items()

    for name, value in items:

        group = value.group

        (groups[group]
         .append(value))

    return sort_dict(groups)



def composedsc(
    robie: Robie,
    cqueue: RobieQueue[RobieCommand],
    mitem: RobieMessage,
    status: dict[str, StatusPluginItem],
) -> None:
    """
    Construct and format message for related chat platform.

    :param robie: Primary class instance for Chatting Robie.
    :param cqueue: Queue instance where the item is received.
    :param mitem: Item containing information for operation.
    :param status: Object containing the status information.
    """

    citem = mitem.reply(
        robie, 'DSC good')

    cqueue.put(citem)



def composeirc(
    robie: Robie,
    cqueue: RobieQueue[RobieCommand],
    mitem: RobieMessage,
    status: dict[str, StatusPluginItem],
) -> None:
    """
    Construct and format message for related chat platform.

    :param robie: Primary class instance for Chatting Robie.
    :param cqueue: Queue instance where the item is received.
    :param mitem: Item containing information for operation.
    :param status: Object containing the status information.
    """

    citem = mitem.reply(
        robie, 'IRC good')

    cqueue.put(citem)



def composemtm(
    robie: Robie,
    cqueue: RobieQueue[RobieCommand],
    mitem: RobieMessage,
    status: dict[str, StatusPluginItem],
) -> None:
    """
    Construct and format message for related chat platform.

    :param robie: Primary class instance for Chatting Robie.
    :param cqueue: Queue instance where the item is received.
    :param mitem: Item containing information for operation.
    :param status: Object containing the status information.
    """

    citem = mitem.reply(
        robie, 'MTM good')

    cqueue.put(citem)
