"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..crypts import arguments



def test_arguments() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    sargs = arguments([
        '--config', 'path'])

    assert sargs == {
        'config': 'path',
        'console': False,
        'debug': False,
        'encrypt': None,
        'decrypt': False}
