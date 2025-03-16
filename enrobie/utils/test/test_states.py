"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from ..states import ClientChannels
from ..states import ClientPublish



def test_ClientChannels() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    channels = ClientChannels()


    attrs = lattrs(channels)

    assert attrs == [
        '_ClientChannels__cached']


    assert inrepr(
        'states.ClientChannels',
        channels)

    assert isinstance(
        hash(channels), int)

    assert instr(
        'states.ClientChannels',
        channels)



def test_ClientChannels_basics() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    channels = ClientChannels()


    channels.create('test')

    select = (
        channels.select('test'))

    assert select is not None

    assert select.endumped == {
        'members': None,
        'title': None,
        'topic': None,
        'unique': 'test'}


    channels.set_title(
        'test', 'Test')

    channels.set_topic(
        'test', 'Test')

    channels.add_member(
        'test', 'mtmbot')

    select = (
        channels.select('Test'))

    assert select is not None

    assert select.endumped == {
        'members': {'mtmbot'},
        'title': 'Test',
        'topic': 'Test',
        'unique': 'test'}


    channels.delete('test')

    select = (
        channels.select('test'))

    assert select is None



def test_ClientChannels_cover() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    channels = ClientChannels()


    channels.create('test')

    channels.add_member(
        'test', 'mtmbot')

    channels.del_member(
        'test', 'mtmbot')

    select = (
        channels.select('test'))

    assert select is not None

    assert select.endumped == {
        'members': None,
        'title': None,
        'topic': None,
        'unique': 'test'}


    channels.add_member(
        'test', 'mtmbot')

    (channels
     .clear_members('test'))

    assert select is not None

    assert select.endumped == {
        'members': None,
        'title': None,
        'topic': None,
        'unique': 'test'}


    channels.set_title(
        'test1', 'Test')

    channels.set_topic(
        'test2', 'Test')

    channels.add_member(
        'test3', 'mtmbot')

    channels.rename_member(
        'mtmbot', 'test')


    select = (
        channels.select('test3'))

    assert select is not None

    assert select.endumped == {
        'members': {'test'},
        'title': None,
        'topic': None,
        'unique': 'test3'}



def test_ClientPublish() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    publish = ClientPublish()


    attrs = lattrs(publish)

    assert attrs == [
        '_ClientPublish__callbacks']


    assert inrepr(
        'states.ClientPublish',
        publish)

    assert isinstance(
        hash(publish), int)

    assert instr(
        'states.ClientPublish',
        publish)
