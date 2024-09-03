"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path



PROJECT = Path(__file__).parent
WORKSPACE = PROJECT.parents[2]
EXAMPLES = PROJECT / 'examples'

VERSION = (
    (PROJECT / 'version.txt')
    .read_text(encoding='utf-8')
    .splitlines()[0].strip())



__version__ = VERSION
