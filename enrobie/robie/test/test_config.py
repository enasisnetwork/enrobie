"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from encommon.types import DictStrAny
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils.sample import ENPYRWS

from . import SAMPLES
from ..config import RobieConfig



def test_RobieConfig(
    tmp_path: Path,
    config: RobieConfig,
    replaces: DictStrAny,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param config: Primary class instance for configuration.
    :param replaces: Mapping of what to replace in samples.
    """


    sample_path = (
        SAMPLES / 'basic.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=config.basic,
        replace=replaces)

    expect = prep_sample(
        content=config.basic,
        replace=replaces)

    assert expect == sample


    sample_path = (
        SAMPLES / 'merge.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=config.merge,
        replace=replaces)

    expect = prep_sample(
        content=config.merge,
        replace=replaces)

    assert expect == sample


    sample_path = (
        SAMPLES / 'config.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=config.config,
        replace=replaces)

    expect = prep_sample(
        content=config.config,
        replace=replaces)

    assert expect == sample
