"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from argparse import ArgumentParser
from sys import argv as sys_argv
from sys import stdin
from typing import Optional

from encommon.types import DictStrAny
from encommon.types.strings import SEMPTY
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


    parser.add_argument(
        '--encrypt',
        help=(
            'encryption operation '
            'that is performed'))


    parser.add_argument(
        '--decrypt',
        action='store_true',
        help=(
            'encryption operation '
            'that is performed'))


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

    sargs = config.sargs
    crypts = config.crypts

    encrypt = sargs['encrypt']
    decrypt = sargs['decrypt']

    _encrypt = crypts.encrypt
    _decrypt = crypts.decrypt

    dashes = '─' * 80

    value: Optional[str] = None


    if encrypt is not None:

        print_ansi(
            'Use <c96>Ctrl-D<c0> '
            'on newline to exit, or '
            'twice on one without')

        print_ansi(
            f'<c32>{dashes}<c0>')

        provide = stdin.read()

        if provide[-1] != '\n':
            print_ansi(SEMPTY)

        print_ansi(
            f'<c32>{dashes}<c0>')

        value = _encrypt(
            value=provide,
            unique=encrypt)

    elif decrypt is not None:

        print_ansi(
            'Paste <c96>encrypted<c0> '
            'crypts string value')

        value = _decrypt(
            value=input())


    assert value is not None

    value = value.rstrip('\n')

    print_ansi(f'<c31>{dashes}<c0>')
    print_ansi(f'<c91>{value}<c0>')
    print_ansi(f'<c31>{dashes}<c0>')



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
        base='execution/crypts',
        status='started')

    operation(config)

    config.logger.log_i(
        base='execution/crypts',
        status='stopped')

    config.logger.stop()



if __name__ == '__main__':
    execution()  # NOCVR
