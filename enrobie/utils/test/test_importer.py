"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..importer import importer



def test_importer() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    dumps = importer('json.dumps')

    assert dumps([1]) == '[1]'
