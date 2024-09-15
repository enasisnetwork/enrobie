"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from encommon.types import DictStrAny
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils.sample import ENPYRWS

from . import SAMPLES
from ..config import RobieConfig
from ..models import RobieMessage
from ..robie import Robie



def test_Robie(
    robie: Robie,
    replaces: DictStrAny,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    :param replaces: Mapping of what to replace in samples.
    """


    attrs = lattrs(robie)

    assert attrs == [
        '_Robie__config',
        '_Robie__logger',
        '_Robie__childs']


    assert inrepr(
        'robie.Robie',
        robie)

    assert hash(robie) > 0

    assert instr(
        'robie.Robie',
        robie)


    assert robie.config

    assert robie.logger

    assert robie.childs

    assert robie.params


    sample_path = (
        SAMPLES / 'dumped.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=robie.dumped,
        replace=replaces)

    expect = prep_sample(
        content=robie.dumped,
        replace=replaces)

    assert expect == sample



def test_Robie_printer(
    robie: Robie,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients

    client = clients['ircbot']

    model = RobieMessage

    item = model(client)

    robie.printer(item)



def test_Robie_cover(
) -> None:
    """
    Perform various tests associated with relevant routines.
    """

    Robie(RobieConfig())
