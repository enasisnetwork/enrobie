"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from sys import flags



PROJECT = Path(__file__).parent

VERSION = (
    (PROJECT / 'version.txt')
    .read_text(encoding='utf-8')
    .splitlines()[0].strip())

BOILER = (
    Path(__file__)
    .read_text(encoding='utf-8')
    .splitlines()[1:5])

WORKSPACE = PROJECT.parents[2]
EXAMPLES = PROJECT / 'examples'



__version__ = VERSION



if flags.optimize:  # NOCVR

    raise RuntimeError(
        'This library must not be'
        ' run in optimized mode,'
        ' assertions are required.')
