"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import TYPE_CHECKING

from encommon.types import BaseModel

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
    from .plugin import HomiePlugin



class HomiePersistRecord(BaseModel, extra='ignore'):
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
        /,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(**data)



class HomiePersist:
    """
    Collect the information using the upstream API endpoint.

    :param plugin: Plugin class instance for Chatting Robie.
    """

    __plugin: 'HomiePlugin'

    __client: HTTPClient

    __location: str


    def __init__(
        self,
        plugin: 'HomiePlugin',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__plugin = plugin

        params = plugin.params

        client = HTTPClient(
            timeout=params.timeout,
            verify=params.ssl_verify,
            capem=params.ssl_capem)

        self.__client = client

        self.__location = (
            f'{params.restful}'
            '/api/persists')


    @property
    def client(
        self,
    ) -> HTTPClient:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__client


    def request(
        self,
    ) -> Response:
        """
        Return the response from upstream API endpoint request.

        :param item: Determine which items will be enumerated.
        :returns: Response from upstream API endpoint request.
        """

        plugin = self.__plugin
        client = self.__client
        params = plugin.params
        location = self.__location

        request = client.request_block

        response = request(
            method='get',
            location=location,
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

            object = model(**item)

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
