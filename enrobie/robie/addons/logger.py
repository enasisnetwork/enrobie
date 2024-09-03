"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread
from typing import Any
from typing import TYPE_CHECKING

from encommon.types import DictStrAny
from encommon.types import clsname

from .queue import RobieQueueItem

if TYPE_CHECKING:
    from ..robie import Robie



class RobieLogger:
    """
    Methods for extending use of underlying logging library.
    """

    __robie: 'Robie'


    def __init__(
        self,
        robie: 'Robie',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__robie = robie


    def start(
        self,
    ) -> None:
        """
        Initialize the Python logging library using parameters.
        """

        robie = self.__robie
        config = robie.config
        logger = config.logger

        logger.start()


    def stop(
        self,
    ) -> None:
        """
        Deinitialize the Python logging library using parameters.
        """

        robie = self.__robie
        config = robie.config
        logger = config.logger

        logger.stop()


    def __process(
        self,
        kwargs: DictStrAny,
    ) -> None:
        """
        Process the keyword arguments handling relevant values.

        :param kwargs: Keyword arguments for populating message.
        """

        base = kwargs.get('base')
        item = kwargs.get('item')
        name = kwargs.get('name')

        threads = (
            RobieQueueItem,
            Thread)

        prefix = '<enrobie.'


        if isinstance(base, threads):
            kwargs['base'] = (
                clsname(base))

        elif str(base)[:9] == prefix:
            kwargs['base'] = (
                clsname(base))


        if isinstance(item, threads):
            kwargs['item'] = (
                clsname(item))

        elif str(item)[:9] == prefix:
            kwargs['item'] = (
                clsname(item))


        if (hasattr(name, 'name')
                and name is not None):
            kwargs['name'] = name.name


    def log(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided keyword arguments into logger object.

        .. note::
           Uses method :py:meth:`encommon.config.Logger.log`.

        :param kwargs: Keyword arguments for populating message.
        """

        robie = self.__robie
        config = robie.config
        logger = config.logger

        self.__process(kwargs)

        logger.log(**kwargs)


    def log_c(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided keyword arguments into logger object.

        .. note::
           Uses method :py:meth:`encommon.config.Logger.log_c`.

        :param kwargs: Keyword arguments for populating message.
        """

        robie = self.__robie
        config = robie.config
        logger = config.logger

        self.__process(kwargs)

        logger.log_c(**kwargs)


    def log_d(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided keyword arguments into logger object.

        .. note::
           Uses method :py:meth:`encommon.config.Logger.log_d`.

        :param kwargs: Keyword arguments for populating message.
        """

        robie = self.__robie
        config = robie.config
        logger = config.logger

        self.__process(kwargs)

        logger.log_d(**kwargs)


    def log_e(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided keyword arguments into logger object.

        .. note::
           Uses method :py:meth:`encommon.config.Logger.log_e`.

        :param kwargs: Keyword arguments for populating message.
        """

        robie = self.__robie
        config = robie.config
        logger = config.logger

        self.__process(kwargs)

        logger.log_e(**kwargs)


    def log_i(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided keyword arguments into logger object.

        .. note::
           Uses method :py:meth:`encommon.config.Logger.log_i`.

        :param kwargs: Keyword arguments for populating message.
        """

        robie = self.__robie
        config = robie.config
        logger = config.logger

        self.__process(kwargs)

        logger.log_i(**kwargs)


    def log_w(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided keyword arguments into logger object.

        .. note::
           Uses method :py:meth:`encommon.config.Logger.log_w`.

        :param kwargs: Keyword arguments for populating message.
        """

        robie = self.__robie
        config = robie.config
        logger = config.logger

        self.__process(kwargs)

        logger.log_w(**kwargs)
