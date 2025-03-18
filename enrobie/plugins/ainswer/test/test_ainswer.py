"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from re import sub as re_sub
from typing import TYPE_CHECKING

from encommon.types import NCTrue
from encommon.utils import read_text
from encommon.utils import save_text
from encommon.utils.sample import ENPYRWS

from enconnect.irc import ClientEvent

from pydantic_ai.models.test import TestModel

from pytest import mark

from . import SAMPLES
from .test_history import _ainswer_history
from ..common import AinswerResponse
from ..history import AinswerHistoryKinds
from ..plugin import AinswerPlugin
from ...logger import LoggerPlugin
from ...logger.test.test_history import _logger_history
from ....clients.irc import IRCClient
from ....clients.irc.message import IRCMessage
from ....clients.irc.test import IRCEVENT_HUBERT_CHAN
from ....clients.irc.test import IRCEVENT_HUBERT_PRIV
from ....clients.irc.test import IRCEVENT_RANDOM_CHAN
from ....clients.irc.test import IRCEVENT_RANDOM_PRIV

if TYPE_CHECKING:
    from ....robie import Robie



def test_AinswerQuestion_engage(
    robie: 'Robie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    plugins = childs.plugins

    plugin = plugins['ainswer']

    assert isinstance(
        plugin, AinswerPlugin)

    question = plugin.question


    testing = TestModel()

    override_agent = (
        plugin.agent
        .override(
            model=testing))

    with override_agent:

        response = (
            question.submit(
                'Hello World!',
                AinswerResponse))

    assert response.text == 'a'



@mark.parametrize(
    'file,kind,event',
    [('random_chanmsg', 'chanmsg',
      IRCEVENT_RANDOM_CHAN),
     ('random_privmsg', 'privmsg',
      IRCEVENT_RANDOM_PRIV),
     ('hubert_chanmsg', 'chanmsg',
      IRCEVENT_HUBERT_CHAN),
     ('hubert_privmsg', 'privmsg',
      IRCEVENT_HUBERT_PRIV)])
def test_AinswerQuestion_prompt(
    robie: 'Robie',
    file: str,
    kind: 'AinswerHistoryKinds',
    event: str,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param file: Name of the file within the samples folder.
    :param kind: What kind of Robie message we dealing with.
    :param event: Raw event received from the network peer.
    :param robie: Primary class instance for Chatting Robie.
    """

    childs = robie.childs
    clients = childs.clients
    plugins = childs.plugins

    client = clients['ircbot']
    plugin = plugins['ainswer']
    logger = plugins['logger']

    assert isinstance(
        client, IRCClient)

    assert isinstance(
        plugin, AinswerPlugin)

    assert isinstance(
        logger, LoggerPlugin)

    question = plugin.question


    item = IRCMessage(
        client,
        ClientEvent(
            client.client,
            event))

    assert item.kind == kind
    assert item.author
    assert item.author == (
        ('hubert', 'hubert')
        if 'hubert' in file
        else ('nick', 'nick'))

    if 'hubert' not in file:
        item.event.author = 'nickname1'
        item.event.recipient = (
            '#enrobie'
            if kind == 'chanmsg'
            else 'ircbot')

    item.event.whome = 'ircbot'

    item.event.message = (
        'Do the thing?')


    _ainswer_history(
        plugin, client)

    _logger_history(
        logger, client)


    sample_path = (
        SAMPLES / f'{file}.txt')

    prompt = (
        question.prompt(
            item,
            'Do the thing!'))

    prompt = re_sub(
        (r'\d{4}\-\d{2}\-\d{2}'
         r'T\d{2}:\d{2}:\d{2}'
         r'(\.\d+)?\+0000'),
        '1980-01-01T00:00:00Z',
        prompt)

    if ENPYRWS is NCTrue:
        save_text(
            sample_path,
            prompt)

    loaded = read_text(
        sample_path)

    assert prompt == loaded
