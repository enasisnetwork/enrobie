"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING
from typing import Type

if TYPE_CHECKING:
    from ..addons import RobieQueueItem
    from ..models import RobieCommand
    from ..models import RobieMessage
    from ..params import RobieParams
    from ..params import RobiePrinterParams
    from ..params import RobieServiceParams
    from ..params import RobieChildParams
    from ..params import RobieClientParams
    from ..params import RobiePersonParams
    from ..params import RobiePluginParams



class RobieModels:
    """
    Return the class object that was imported within method.
    """


    @classmethod
    def robie(
        cls,
    ) -> Type['RobieParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from ..params import (
            RobieParams)

        return RobieParams


    @classmethod
    def printer(
        cls,
    ) -> Type['RobiePrinterParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from ..params import (
            RobiePrinterParams)

        return RobiePrinterParams


    @classmethod
    def service(
        cls,
    ) -> Type['RobieServiceParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from ..params import (
            RobieServiceParams)

        return RobieServiceParams


    @classmethod
    def child(
        cls,
    ) -> Type['RobieChildParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from ..params import (
            RobieChildParams)

        return RobieChildParams


    @classmethod
    def client(
        cls,
    ) -> Type['RobieClientParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from ..params import (
            RobieClientParams)

        return RobieClientParams


    @classmethod
    def plugin(
        cls,
    ) -> Type['RobiePluginParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from ..params import (
            RobiePluginParams)

        return RobiePluginParams


    @classmethod
    def person(
        cls,
    ) -> Type['RobiePersonParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from ..params import (
            RobiePersonParams)

        return RobiePersonParams


    @classmethod
    def queue(
        cls,
    ) -> Type['RobieQueueItem']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from ..addons import (
            RobieQueueItem)

        return RobieQueueItem


    @classmethod
    def message(
        cls,
    ) -> Type['RobieMessage']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from ..models import (
            RobieMessage)

        return RobieMessage


    @classmethod
    def command(
        cls,
    ) -> Type['RobieCommand']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from ..models import (
            RobieCommand)

        return RobieCommand
