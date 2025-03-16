"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from .test_client import DSCEVENTS
from .test_client import DSCEVENT_HUBERT_CHAN
from .test_client import DSCEVENT_HUBERT_PRIV
from .test_client import DSCEVENT_RANDOM_CHAN
from .test_client import DSCEVENT_RANDOM_PRIV



__all__ = [
    'DSCEVENTS',
    'DSCEVENT_HUBERT_CHAN',
    'DSCEVENT_HUBERT_PRIV',
    'DSCEVENT_RANDOM_CHAN',
    'DSCEVENT_RANDOM_PRIV']



SAMPLES = (
    Path(__file__).parent
    / 'samples')
