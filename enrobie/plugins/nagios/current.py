"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Literal
from typing import TYPE_CHECKING

from encommon.times import Time
from encommon.types import BaseModel

from enconnect.utils import HTTPClient

from httpx import Response

from pydantic import Field

if TYPE_CHECKING:
    from .plugin import NagiosPlugin



_FIELDS = {
    'status': 'last_hard_state',
    'description': 'description',
    'downtime': 'scheduled_downtime_depth',
    'handled': 'problem_has_been_acknowledged',
    'checked': 'last_check'}



class NagiosCurrentObject(BaseModel, extra='forbid'):
    """
    Information regarding the item within Nagios monitoring.
    """

    name: Annotated[
        str,
        Field(...,
              description='Name of the object in Nagios',
              min_length=1)]

    status: Annotated[
        str,
        Field(...,
              description='Current status for the object',
              min_length=1)]

    latest: Annotated[
        str,
        Field(...,
              description='When the latest event occurred',
              min_length=1)]

    downtime: Annotated[
        bool,
        Field(...,
              description='Whether in scheduled downtime')]

    handled: Annotated[
        bool,
        Field(...,
              description='Whether or not if was handled')]



class NagiosCurrentHost(NagiosCurrentObject, extra='forbid'):
    """
    Information regarding the item within Nagios monitoring.
    """



class NagiosCurrentService(NagiosCurrentObject, extra='forbid'):
    """
    Information regarding the item within Nagios monitoring.
    """

    host: Annotated[
        str,
        Field(...,
              description='Host the service is related to',
              min_length=1)]



class NagiosCurrentRecords(BaseModel, extra='forbid'):
    """
    Summarized information regarding the items within Nagios.
    """

    hosts: Annotated[
        list[NagiosCurrentHost],
        Field(...,
              description='System related status values')]

    services: Annotated[
        list[NagiosCurrentService],
        Field(...,
              description='Service related status values')]



class NagiosCurrentSummary(BaseModel, extra='forbid'):
    """
    Summarized information regarding the items within Nagios.
    """

    service_normal: Annotated[
        int,
        Field(...,
              description='Object count in normal state',
              ge=0)]

    service_issues: Annotated[
        int,
        Field(...,
              description='Object count in issue state',
              ge=0)]

    host_normal: Annotated[
        int,
        Field(...,
              description='Object count in normal state',
              ge=0)]

    host_issues: Annotated[
        int,
        Field(...,
              description='Object count in issue state',
              ge=0)]



class NagiosCurrent:
    """
    Collect the information using the upstream API endpoint.

    :param plugin: Plugin class instance for Chatting Robie.
    """

    __plugin: 'NagiosPlugin'


    def __init__(
        self,
        plugin: 'NagiosPlugin',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__plugin = plugin


    def request(
        self,
        item: Literal['host', 'service'],
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
                '/cgi-bin/statusjson.cgi'),
            httpauth=(
                (params.username,
                 params.password)
                if params.username
                and params.password
                else None),
            timeout=params.timeout,
            params={
                'query': f'{item}list',
                'formatoptions': 'enumerate',
                'details': 'true'})

        (response
         .raise_for_status())


        return response


    @property
    def hosts(
        self,
    ) -> list[NagiosCurrentHost]:
        """
        Return the response from upstream API endpoint request.

        :returns: Response from upstream API endpoint request.
        """

        returned: list[NagiosCurrentHost] = []

        model = NagiosCurrentHost


        response = self.request('host')


        items = (
            response.json()
            ['data']['hostlist']
            .items())

        for name, values in items:

            checked = values[
                _FIELDS['checked']]

            latest = Time(
                checked / 1000,
                tzname='US/Central')

            status = values[
                _FIELDS['status']]

            downtime = values[
                _FIELDS['downtime']]

            handled = values[
                _FIELDS['handled']]

            object = model(
                name=name,
                status=status,
                latest=latest.human,
                downtime=downtime,
                handled=handled)

            returned.append(object)


        return returned


    @property
    def services(
        self,
    ) -> list[NagiosCurrentService]:
        """
        Return the response from upstream API endpoint request.

        :returns: Response from upstream API endpoint request.
        """

        returned: list[NagiosCurrentService] = []

        model = NagiosCurrentService


        response = self.request('service')


        items = (
            response.json()
            ['data']['servicelist']
            .items())


        for host, _values in items:

            _items = _values.values()

            for values in _items:

                checked = values[
                    _FIELDS['checked']]

                latest = Time(
                    checked / 1000,
                    tzname='US/Central')

                name = values[
                    _FIELDS['description']]

                status = values[
                    _FIELDS['status']]

                downtime = values[
                    _FIELDS['downtime']]

                handled = values[
                    _FIELDS['handled']]

                object = model(
                    name=name,
                    host=host,
                    status=status,
                    latest=latest.human,
                    downtime=downtime,
                    handled=handled)

                returned.append(object)


        return returned


    @property
    def summary(
        self,
    ) -> NagiosCurrentSummary:
        """
        Return the response from upstream API endpoint request.

        :returns: Response from upstream API endpoint request.
        """

        normal = {'host': 0, 'service': 0}
        issues = {'host': 0, 'service': 0}

        for host in self.hosts:

            target = (
                normal
                if host.status == 'up'
                else issues)

            target['host'] += 1

        for srvc in self.services:

            target = (
                normal
                if srvc.status == 'ok'
                else issues)

            target['service'] += 1

        return NagiosCurrentSummary(
            service_normal=normal['service'],
            service_issues=issues['service'],
            host_normal=normal['host'],
            host_issues=issues['host'])


    @property
    def records(
        self,
    ) -> NagiosCurrentRecords:
        """
        Return the response from upstream API endpoint request.

        :returns: Response from upstream API endpoint request.
        """

        return NagiosCurrentRecords(
            services=self.services,
            hosts=self.hosts)
