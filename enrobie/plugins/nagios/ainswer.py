"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio

from encommon.types import funcname

from pydantic_ai import RunContext

from .current import NagiosCurrentRecords
from ..ainswer import AinswerDepends



async def nagios_current(
    context: RunContext[AinswerDepends],
) -> list[NagiosCurrentRecords]:
    """
    Return the current status for infratstructure in Nagios.

    .. note::
       This tool will return status values from Nagios Core.
       Nagios is a network and system monitoring platform.

    :returns: Current status for infratstructure in Nagios.
    """

    from .plugin import NagiosPlugin

    deps = context.deps
    ainswer = deps.plugin
    mitem = deps.mitem

    assert ainswer.thread

    assert mitem is not None

    thread = ainswer.thread

    plugins = (
        thread.service
        .plugins.childs
        .values())


    returned: list[NagiosCurrentRecords] = []


    for plugin in plugins:

        related = isinstance(
            plugin, NagiosPlugin)

        if related is False:
            continue

        assert isinstance(
            plugin, NagiosPlugin)

        # Basic trust enforcement
        if plugin.notrust(mitem):
            continue

        returned.append(
            plugin.current
            .records)


    await asyncio.sleep(0)

    ainswer.printer({
        'Function': funcname(),
        'Returned': returned})

    return returned
