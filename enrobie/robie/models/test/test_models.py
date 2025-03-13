"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..robie import RobieModels



def test_RobieModels_cover() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    models = RobieModels

    assert models.robie()
    assert models.printer()
    assert models.service()

    assert models.child()
    assert models.client()
    assert models.plugin()
    assert models.person()

    assert models.queue()
    assert models.message()
    assert models.command()
