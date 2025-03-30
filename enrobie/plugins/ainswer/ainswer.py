"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from typing import Optional

from encommon.types import funcname

from pydantic_ai import RunContext

from .common import AinswerDepends
from .memory import AinswerMemoryMessageField
from .memory import AinswerMemoryRecord
from .memory import AinswerMemoryUniqueField



NOTAPERSON = Exception(
    'User is not a Robie person')



async def ainswer_memory_insert(
    context: RunContext[AinswerDepends],
    message: AinswerMemoryMessageField,
) -> None:
    """
    Insert the memory into the historical person memorables.

    Do not add memories of previous questions or discussion.
    Do not add new memories without confirmation as there is
    limited storage that the person may have for memorables.
    Only add the memory one time after ensuring it does not
    already exist, using the `ainswer_memory_records` tool.
    Always confirm with the person before inserting message.
    Be very cautious and conservative with use of this tool,
    the bot is configured by default to remove older entries
    once the limit for the person memories has been reached!

    .. note::
       This tool will allow for inserting new memories for
       the provided username, also known as a Robie person.
    """

    deps = context.deps
    ainswer = deps.plugin
    mitem = deps.mitem
    memory = ainswer.memory

    inputted = {
        'message': message}

    await asyncio.sleep(0)


    # Because of TestModel
    if mitem is None:
        return None


    _person = mitem.person

    if _person is None:
        return None

    memory.insert(
        person=_person,
        message=message)


    ainswer.printer({
        'Function': funcname(),
        'Inputted': inputted})



async def ainswer_memory_records(
    context: RunContext[AinswerDepends],
) -> Optional[list[AinswerMemoryRecord]]:
    """
    Return the historical records for the person memorables.

    .. note::
       This tool will return historical memorable items for
       the provided username, also known as a Robie person.
    """

    deps = context.deps
    ainswer = deps.plugin
    mitem = deps.mitem


    await asyncio.sleep(0)

    # Because of TestModel
    if mitem is None:
        return None


    _person = mitem.person

    if _person is None:
        return None

    returned = (
        ainswer.memory
        .records(mitem))


    ainswer.printer({
        'Function': funcname(),
        'Returned': returned})

    return returned



async def ainswer_memory_delete(
    context: RunContext[AinswerDepends],
    unique: AinswerMemoryUniqueField,
) -> None:
    """
    Delete the record from the historical person memorables.

    .. note::
       This tool will allow for deleting the memories for
       the provided username, also known as a Robie person.
    """

    deps = context.deps
    ainswer = deps.plugin
    mitem = deps.mitem
    memory = ainswer.memory

    inputted = {
        'unique': unique}


    await asyncio.sleep(0)

    # Because of TestModel
    if mitem is None:
        return None


    _person = mitem.person

    if _person is None:
        return None

    memory.delete(
        _person, unique)


    ainswer.printer({
        'Function': funcname(),
        'Inputted': inputted})
