"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.utils import fuzz_match

from .child import RobieChild
from ..models import RobieModels

if TYPE_CHECKING:
    from .client import RobieClient
    from ..params import RobiePersonParams



class RobiePerson(RobieChild):
    """
    Contain the properties regarding the actual user person.
    """


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        # Review the parameters


    @property
    def kind(
        self,
    ) -> Literal['person']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'person'


    @property
    def params(
        self,
    ) -> 'RobiePersonParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            RobieModels
            .person())

        params = super().params

        assert isinstance(
            params, model)

        return params


    @property
    def first(
        self,
    ) -> Optional[str]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.params.first


    @property
    def last(
        self,
    ) -> Optional[str]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.params.last


    @property
    def about(
        self,
    ) -> Optional[str]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.params.about


    @property
    def weight(
        self,
    ) -> int:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.params.weight


    def match(
        self,
        client: 'RobieClient',
        check: str,
    ) -> bool:
        """
        Return the boolean indicating whether check is a match.

        :param client: Client class instance for Chatting Robie.
        :param check: Value to be searched within the haystack.
        :returns: Boolean indicating whether check is a match.
        """

        params = self.params

        name = client.name
        matches = params.matches

        matched: set[bool] = set()

        for match in matches:

            name = match.client
            patterns = match.match

            if client.name != name:
                continue

            fuzz = fuzz_match(
                check, patterns)

            matched.add(fuzz)

        return any(matched)
