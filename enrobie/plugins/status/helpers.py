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

if TYPE_CHECKING:
    from ...robie.childs import RobieClient
    from ...robie.models import RobieMessage
    from .common import StatusPluginItem
    from .params import StatusPluginReportParams
    from .plugin import StatusPlugin



def grouped(
    plugin: 'StatusPlugin',
) -> dict[str, list['StatusPluginItem']]:
    """
    Return the dictionary with status value stored by group.

    :param plugin: Plugin class instance for Chatting Robie.
    :returns: Dictionary with status value stored by group.
    """

    status = plugin.status

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
    params = plugin.params
    member = thread.member
    cqueue = member.cqueue

    compose: list[str] = []


    def _compose(
        message: str,
    ) -> None:

        citem = mitem.reply(
            robie, message)

        cqueue.put(citem)


    def _format() -> None:

        epoch = int(value.time)

        sicon = (
            (getattr(
                params.icons,
                value.state)
             .dsc)
            or SEMPTY)

        sicon = (
            f'{sicon} '
            if len(sicon) >= 1
            else sicon)

        vicon = (
            value.icon.dsc
            or SEMPTY)

        compose.append(
            (f'{vicon or ""} '
             f'{value.title}/'
             f'`{value.unique}`:'
             f' {sicon or ""}'
             f'`{value.state}` '
             f'<t:{epoch}:R>')
            .strip())


    items = sorted(
        grouped(plugin)
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



def reportdsc(
    plugin: 'StatusPlugin',
    client: 'RobieClient',
    status: 'StatusPluginItem',
    report: 'StatusPluginReportParams',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param client: Client class instance for Chatting Robie.
    :param status: Object containing the status information.
    :param report: Object containing the report information.
    """

    assert plugin.thread

    thread = plugin.thread
    params = plugin.params
    member = thread.member
    cqueue = member.cqueue


    def _compose(
        message: str,
    ) -> None:

        citem = (
            client.compose(
                report.target,
                message))

        cqueue.put(citem)


    epoch = int(status.time)

    sicon = (
        (getattr(
            params.icons,
            status.state)
         .dsc)
        or SEMPTY)

    sicon = (
        f'{sicon} '
        if len(sicon) >= 1
        else sicon)

    vicon = (
        status.icon.dsc
        or SEMPTY)

    _compose(
        (f'{vicon or ""} '
         f'{status.title}/'
         f'`{status.unique}`:'
         f' {sicon or ""}'
         f'`{status.state}` '
         f'<t:{epoch}:R>')
        .strip())



def composeirc(
    plugin: 'StatusPlugin',
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
    params = plugin.params
    member = thread.member
    cqueue = member.cqueue


    def _compose(
        message: str,
    ) -> None:

        citem = mitem.reply(
            robie, message)

        cqueue.put(citem)


    def _format() -> None:

        durate = Duration(
            value.time.since)

        sicon = (
            (getattr(
                params.icons,
                value.state)
             .irc)
            or SEMPTY)

        sicon = (
            f'{sicon} '
            if len(sicon) >= 1
            else sicon)

        vicon = (
            value.icon.irc
            or SEMPTY)

        _compose(
            (f'{vicon or ""} '
             f'{value.title}/'
             f'{value.unique}:'
             f' {sicon or ""}'
             f'{value.state} '
             f'for {durate}')
            .strip())


    items = sorted(
        grouped(plugin)
        .items())

    for name, values in items:

        _compose(name)

        _values = sorted(values)

        for value in _values:
            _format()



def reportirc(
    plugin: 'StatusPlugin',
    client: 'RobieClient',
    status: 'StatusPluginItem',
    report: 'StatusPluginReportParams',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param client: Client class instance for Chatting Robie.
    :param status: Object containing the status information.
    :param report: Object containing the report information.
    """

    assert plugin.thread

    thread = plugin.thread
    params = plugin.params
    member = thread.member
    cqueue = member.cqueue


    def _compose(
        message: str,
    ) -> None:

        citem = (
            client.compose(
                report.target,
                message))

        cqueue.put(citem)


    durate = Duration(
        status.time.since)

    sicon = (
        (getattr(
            params.icons,
            status.state)
         .irc)
        or SEMPTY)

    sicon = (
        f'{sicon} '
        if len(sicon) >= 1
        else sicon)

    vicon = (
        status.icon.irc
        or SEMPTY)

    _compose(
        (f'{vicon or ""} '
         f'{status.title}/'
         f'{status.unique}:'
         f' {sicon or ""}'
         f'{status.state} '
         f'for {durate}')
        .strip())



def composemtm(
    plugin: 'StatusPlugin',
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
    params = plugin.params
    member = thread.member
    cqueue = member.cqueue

    compose: list[str] = []


    def _compose(
        message: str,
    ) -> None:

        citem = mitem.reply(
            robie, message)

        cqueue.put(citem)


    def _format() -> None:

        durate = Duration(
            value.time.since)

        sicon = (
            (getattr(
                params.icons,
                value.state)
             .mtm)
            or SEMPTY)

        sicon = (
            f'{sicon} '
            if len(sicon) >= 1
            else sicon)

        vicon = (
            value.icon.mtm
            or SEMPTY)

        compose.append(
            (f'{vicon or ""} '
             f'{value.title}/'
             f'`{value.unique}`:'
             f' {sicon or ""}'
             f'`{value.state}` '
             f'for `{durate}`')
            .strip())


    items = sorted(
        grouped(plugin)
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



def reportmtm(
    plugin: 'StatusPlugin',
    client: 'RobieClient',
    status: 'StatusPluginItem',
    report: 'StatusPluginReportParams',
) -> None:
    """
    Construct and format message for related chat platform.

    :param plugin: Plugin class instance for Chatting Robie.
    :param client: Client class instance for Chatting Robie.
    :param status: Object containing the status information.
    :param report: Object containing the report information.
    """

    assert plugin.thread

    thread = plugin.thread
    params = plugin.params
    member = thread.member
    cqueue = member.cqueue


    def _compose(
        message: str,
    ) -> None:

        citem = (
            client.compose(
                report.target,
                message))

        cqueue.put(citem)


    durate = Duration(
        status.time.since)

    sicon = (
        (getattr(
            params.icons,
            status.state)
         .mtm)
        or SEMPTY)

    sicon = (
        f'{sicon} '
        if len(sicon) >= 1
        else sicon)

    vicon = (
        status.icon.mtm
        or SEMPTY)

    _compose(
        (f'{vicon or ""} '
         f'{status.title}/'
         f'`{status.unique}`:'
         f' {sicon or ""}'
         f'`{status.state}` '
         f'for `{durate}`')
        .strip())
