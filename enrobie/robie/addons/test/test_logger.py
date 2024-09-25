"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread
from typing import TYPE_CHECKING

from _pytest.logging import LogCaptureFixture

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

if TYPE_CHECKING:
    from ...robie import Robie



def test_RobieLogger(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    logger = robie.logger


    attrs = lattrs(logger)

    assert attrs == [
        '_RobieLogger__robie']


    assert inrepr(
        'logger.RobieLogger',
        logger)

    assert isinstance(
        hash(logger), int)

    assert instr(
        'logger.RobieLogger',
        logger)



def test_RobieLogger_message(
    robie: 'Robie',
    caplog: LogCaptureFixture,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    :param caplog: pytest object for capturing log message.
    """

    logger = robie.logger


    logger.start()

    logger.log_d(about='pytest')
    logger.log_c(about='pytest')
    logger.log_e(about='pytest')
    logger.log_i(about='pytest')
    logger.log_w(about='pytest')

    logger.log(
        level='debug',
        about='pytest')

    logger.stop()

    output = caplog.record_tuples

    assert len(output) == 6

    logger.log_d(about='pytest')
    logger.log_c(about='pytest')
    logger.log_e(about='pytest')
    logger.log_i(about='pytest')
    logger.log_w(about='pytest')

    output = caplog.record_tuples

    assert len(output) == 6



def test_RobieLogger_cover(
    robie: 'Robie',
    caplog: LogCaptureFixture,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    :param caplog: pytest object for capturing log message.
    """

    logger = robie.logger
    childs = robie.childs
    clients = childs.clients


    thread = Thread(name='foo')

    client = clients['ircbot']


    logger.log_i(base=thread)
    logger.log_i(item=thread)
    logger.log_i(base=robie)
    logger.log_i(item=robie)
    logger.log_i(name=client)
