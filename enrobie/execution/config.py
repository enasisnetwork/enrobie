"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from argparse import ArgumentParser
from sys import argv as sys_argv
from typing import Optional

from encommon.types import DictStrAny
from encommon.utils import array_ansi
from encommon.utils import print_ansi

from ..robie import RobieConfig



def arguments(
    args: Optional[list[str]] = None,
) -> DictStrAny:
    """
    Construct arguments which are associated with the file.

    :param args: Override the source for the main arguments.
    :returns: Construct arguments from command line options.
    """

    parser = ArgumentParser()

    args = args or sys_argv[1:]


    parser.add_argument(
        '--config',
        required=True,
        help=(
            'complete or relative '
            'path to config file'))


    parser.add_argument(
        '--console',
        action='store_true',
        default=False,
        help=(
            'write log messages '
            'to standard output'))


    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help=(
            'increase logging level '
            'for standard output'))


    return vars(
        parser
        .parse_args(args))



def operation(
    # NOCVR
    config: RobieConfig,
) -> None:
    """
    Perform whatever operation is associated with the file.

    :param config: Primary class instance for configuration.
    """

    dumped = config.config

    print_ansi(
        array_ansi(dumped))



def execution(
    # NOCVR
    args: Optional[list[str]] = None,
) -> None:
    """
    Perform whatever operation is associated with the file.

    :param args: Override the source for the main arguments.
    """

    config = RobieConfig(
        arguments(args))

    config.logger.start()

    config.logger.log_i(
        base='execution/config',
        status='started')

    operation(config)

    config.logger.log_i(
        base='execution/config',
        status='stopped')

    config.logger.stop()



if __name__ == '__main__':
    execution()  # NOCVR
