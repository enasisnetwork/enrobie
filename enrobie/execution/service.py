"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from argparse import ArgumentParser
from signal import SIGHUP
from signal import SIGINT
from signal import SIGTERM
from signal import signal
from sys import argv as sys_argv
from typing import Optional

from encommon.types import DictStrAny

from ..clients import DSCClient
from ..clients import DSCClientParams
from ..clients import IRCClient
from ..clients import IRCClientParams
from ..clients import MTMClient
from ..clients import MTMClientParams
from ..plugins import StatusPlugin
from ..plugins import StatusPluginParams
from ..robie import Robie
from ..robie import RobieConfig
from ..robie import RobieService



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


    parser.add_argument(
        '--print_message',
        action='store_true',
        default=False,
        dest='pmessage',
        help=(
            'print the received '
            'messages to console'))


    parser.add_argument(
        '--print_command',
        action='store_true',
        default=False,
        dest='pcommand',
        help=(
            'print the submited '
            'commands to console'))


    return vars(
        parser
        .parse_args(args))



def operation(
    # NOCVR
    robie: Robie,
) -> None:
    """
    Perform whatever operation is associated with the file.

    :param robie: Primary class instance for Chatting Robie.
    """

    service = RobieService(robie)

    service.start()

    signal(SIGINT, service.soft)
    signal(SIGTERM, service.soft)
    signal(SIGHUP, service.soft)

    service.operate()



def register_params(
    # NOCVR
    config: RobieConfig,
) -> None:
    """
    Register the plugin parameters for parameter processing.

    :param config: Primary class instance for configuration.
    """

    config.register(
        name='ircbot',
        client=IRCClientParams)

    config.register(
        name='dscbot',
        client=DSCClientParams)

    config.register(
        name='mtmbot',
        client=MTMClientParams)

    config.register(
        name='status',
        plugin=StatusPluginParams)



def register_plugins(
    # NOCVR
    robie: Robie,
) -> None:
    """
    Register the plugin parameters for parameter processing.

    :param robie: Primary class instance for Chatting Robie.
    """

    robie.register(
        name='ircbot',
        client=IRCClient)

    robie.register(
        name='dscbot',
        client=DSCClient)

    robie.register(
        name='mtmbot',
        client=MTMClient)

    robie.register(
        name='status',
        plugin=StatusPlugin)



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

    register_params(config)

    config.logger.start()

    config.logger.log_i(
        base='execution/service',
        status='started')

    robie = Robie(config)

    register_plugins(robie)

    operation(robie)

    config.logger.log_i(
        base='execution/service',
        status='stopped')

    config.logger.stop()



if __name__ == '__main__':
    execution()  # NOCVR
