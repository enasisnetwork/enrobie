"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import BaseModel
from encommon.types import DictStrAny

from enconnect.utils import HTTPClient

from enhomie.homie.addons.persist import _FIELD_ABOUT
from enhomie.homie.addons.persist import _FIELD_ABOUT_LABEL
from enhomie.homie.addons.persist import _FIELD_EXPIRE
from enhomie.homie.addons.persist import _FIELD_LEVEL
from enhomie.homie.addons.persist import _FIELD_TAGS
from enhomie.homie.addons.persist import _FIELD_UNIQUE
from enhomie.homie.addons.persist import _FIELD_UPDATE
from enhomie.homie.addons.persist import _FIELD_VALUE
from enhomie.homie.addons.persist import _FIELD_VALUE_LABEL
from enhomie.homie.addons.persist import _FIELD_VALUE_UNIT

from httpx import Response

if TYPE_CHECKING:
    from ...robie.models import RobieMessage
    from .plugin import HomiePlugin



class HomiePersistRecord(BaseModel, extra='forbid'):
    """
    Information relevant to Homie Automate persistent value.
    """

    unique: _FIELD_UNIQUE

    value: _FIELD_VALUE

    value_unit: _FIELD_VALUE_UNIT

    value_label: _FIELD_VALUE_LABEL

    about: _FIELD_ABOUT

    about_label: _FIELD_ABOUT_LABEL

    level: _FIELD_LEVEL

    tags: _FIELD_TAGS

    expire: _FIELD_EXPIRE

    update: _FIELD_UPDATE


    def __init__(
        self,
        entry: DictStrAny,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        data = {
            k: v for k, v
            in entry.items()
            if k in [
                'unique',
                'value',
                'value_unit',
                'value_label',
                'about',
                'about_label',
                'level',
                'tags',
                'expire',
                'update']}

        super().__init__(**data)



class HomiePersist:
    """
    Collect the information using the upstream API endpoint.

    :param plugin: Plugin class instance for Chatting Robie.
    """

    __plugin: 'HomiePlugin'


    def __init__(
        self,
        plugin: 'HomiePlugin',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__plugin = plugin


    def request(
        self,
    ) -> Response:
        """
        Return the response from upstream API endpoint request.

        :param item: Determine which items will be enumerated.
        :returns: Response from upstream API endpoint request.
        """

        plugin = self.__plugin
        params = plugin.params


        client = HTTPClient(
            timeout=params.timeout,
            verify=params.ssl_verify,
            capem=params.ssl_capem)

        request = client.request_block

        response = request(
            method='get',
            location=(
                f'{params.restful}'
                '/api/persists'),
            httpauth=(
                (params.username,
                 params.password)
                if params.username
                and params.password
                else None),
            timeout=params.timeout)

        (response
         .raise_for_status())


        return response


    @property
    def records(
        self,
    ) -> list[HomiePersistRecord]:
        """
        Return the response from upstream API endpoint request.

        :returns: Response from upstream API endpoint request.
        """

        returned: list[HomiePersistRecord] = []

        model = HomiePersistRecord


        response = self.request()


        items = (
            response.json()
            ['entries'])

        for item in items:

            object = model(item)

            returned.append(object)


        return returned


    def record(
        self,
        unique: str,
    ) -> HomiePersistRecord:
        """
        Return the response from upstream API endpoint request.

        :param unique: Unique identifier from within the table.
        :returns: Response from upstream API endpoint request.
        """

        records = self.records


        for record in records:

            _unique = record.unique

            if _unique != unique:
                continue

            return record


        raise ValueError('unique')



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
        persist.record(unique))

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
        persist.record(unique))

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
        persist.record(unique))

    citem = mitem.reply(
        robie, str(current))

    cqueue.put(citem)
