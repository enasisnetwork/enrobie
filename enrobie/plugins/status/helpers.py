"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.times import Duration
from encommon.types import DictStrAny
from encommon.types import sort_dict
from encommon.types.strings import NEWLINE
from encommon.types.strings import SEMPTY

from .common import StatusPluginItem
from .params import StatusPluginParams
from ...robie.addons import RobieQueue
from ...robie.models import RobieCommand
from ...robie.models import RobieMessage

if TYPE_CHECKING:
    from .plugin import StatusPlugin



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
    plugin: 'StatusPlugin',
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

    robie = plugin.robie
    params = plugin.params

    compose: list[str] = []


    def _compose(
        message: str,
    ) -> None:

        citem = mitem.reply(
            robie, message)

        cqueue.put(citem)


    def _format() -> None:

        assert isinstance(
            params,
            StatusPluginParams)

        epoch = int(value.time)

        sicon = (
            (getattr(
                params.icons,
                value.state)
             .dsc)
            or SEMPTY)

        vicon = (
            value.icon.dsc
            or SEMPTY)

        compose.append(
            (f'{vicon or ""} '
             f'{value.title}/'
             f'`{value.unique}`:'
             f' {sicon or ""}'
             f' `{value.state}` '
             f'<t:{epoch}:R>')
            .strip())


    items = sorted(
        grouped(status)
        .items())

    for name, values in items:

        compose.append(
            f'**{name}**')

        _values = sorted(values)

        for value in _values:
            _format()

    _compose(
        NEWLINE
        .join(compose))



def composeirc(
    plugin: 'StatusPlugin',
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

    robie = plugin.robie
    params = plugin.params


    def _compose(
        message: str,
    ) -> None:

        citem = mitem.reply(
            robie, message)

        cqueue.put(citem)


    def _format() -> None:

        assert isinstance(
            params,
            StatusPluginParams)

        durate = Duration(
            value.time.since)

        sicon = (
            (getattr(
                params.icons,
                value.state)
             .irc)
            or SEMPTY)

        vicon = (
            value.icon.irc
            or SEMPTY)

        _compose(
            (f'{vicon or ""} '
             f'{value.title}/'
             f'{value.unique}:'
             f' {sicon or ""}'
             f' {value.state} '
             f'for {durate}')
            .strip())


    items = sorted(
        grouped(status)
        .items())

    for name, values in items:

        _compose(name)

        _values = sorted(values)

        for value in _values:
            _format()



def composemtm(
    plugin: 'StatusPlugin',
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

    robie = plugin.robie
    params = plugin.params

    compose: list[str] = []


    def _compose(
        message: str,
    ) -> None:

        citem = mitem.reply(
            robie, message)

        cqueue.put(citem)


    def _format() -> None:

        assert isinstance(
            params,
            StatusPluginParams)

        durate = Duration(
            value.time.since)

        sicon = (
            (getattr(
                params.icons,
                value.state)
             .mtm)
            or SEMPTY)

        vicon = (
            value.icon.mtm
            or SEMPTY)

        compose.append(
            (f'{vicon or ""} '
             f'{value.title}/'
             f'`{value.unique}`:'
             f' {sicon or ""}'
             f' `{value.state}` '
             f'for `{durate}`')
            .strip())


    items = sorted(
        grouped(status)
        .items())

    for name, values in items:

        compose.append(
            f'**{name}**')

        _values = sorted(values)

        for value in _values:
            _format()

    _compose(
        NEWLINE
        .join(compose))
