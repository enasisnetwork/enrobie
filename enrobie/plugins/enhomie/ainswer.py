"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio

from encommon.types import funcname

from pydantic_ai import RunContext

from .persist import HomiePersistRecord
from ..ainswer import AinswerDepends



async def homie_persist(
    context: RunContext[AinswerDepends],
) -> list[HomiePersistRecord]:
    """
    Return the current values in Homie Automate persistence.

    .. note::
       This tool will return values from the Homie Automate
       persistence store. They may include information about
       many things regarding the Robie owner home status.

    :returns: Current values in Homie Automate persistence.
    """

    from .plugin import HomiePlugin

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


    returned: list[HomiePersistRecord] = []


    for plugin in plugins:

        related = isinstance(
            plugin, HomiePlugin)

        if related is False:
            continue

        assert isinstance(
            plugin, HomiePlugin)

        # Basic trust enforcement
        if plugin.notrust(mitem):
            continue

        returned.extend(
            plugin.persist
            .records)


    await asyncio.sleep(0)

    ainswer.printer({
        'Function': funcname(),
        'Returned': returned})

    return returned
