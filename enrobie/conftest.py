"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from encommon.types import DictStrAny
from encommon.utils import save_text

from enconnect.fixtures import client_dscsock
from enconnect.fixtures import client_ircsock
from enconnect.fixtures import client_mtmsock

from pytest import fixture

from . import EXAMPLES
from . import PROJECT
from .robie import Robie
from .robie import RobieConfig
from .robie import RobieService



__all__ = [
    'client_dscsock',
    'client_ircsock',
    'client_mtmsock']



def config_factory(
    tmp_path: Path,
) -> RobieConfig:
    """
    Construct the instance for use in the downstream tests.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: Newly constructed instance of related class.
    """

    content = (
        f"""

        enconfig:
          paths:
            - {EXAMPLES}
            - {tmp_path}/robie

        enlogger:
          stdo_level: info

        database: >-
          sqlite:///{tmp_path}/db

        """)

    config_path = (
        tmp_path / 'config.yml')

    save_text(
        config_path, content)

    sargs = {
        'config': config_path,
        'console': True,
        'debug': True,
        'pmessage': True,
        'pcommand': True}

    return RobieConfig(sargs)



@fixture
def config(
    tmp_path: Path,
) -> RobieConfig:
    """
    Construct the instance for use in the downstream tests.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: Newly constructed instance of related class.
    """

    return config_factory(tmp_path)



@fixture
def replaces(
    tmp_path: Path,
) -> DictStrAny:
    """
    Return the complete mapping of what replaced in sample.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: Complete mapping of what replaced in sample.
    """

    return {
        'PROJECT': PROJECT,
        'TMPPATH': tmp_path}



def robie_factory(
    config: RobieConfig,
) -> Robie:
    """
    Construct the instance for use in the downstream tests.

    :param config: Primary class instance for configuration.
    :returns: Newly constructed instance of related class.
    """

    return Robie(config)



@fixture
def robie(
    config: RobieConfig,
) -> Robie:
    """
    Construct the instance for use in the downstream tests.

    :param config: Primary class instance for configuration.
    :returns: Newly constructed instance of related class.
    """

    return robie_factory(config)



def service_factory(
    robie: Robie,
) -> RobieService:
    """
    Construct the instance for use in the downstream tests.

    :param robie: Primary class instance for Chatting Robie.
    :returns: Newly constructed instance of related class.
    """

    return RobieService(robie)



@fixture
def service(
    robie: Robie,
) -> RobieService:
    """
    Construct the instance for use in the downstream tests.

    :param robie: Primary class instance for Chatting Robie.
    :returns: Newly constructed instance of related class.
    """

    return service_factory(robie)
