"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from .test_client import IRCEVENTS
from .test_client import IRCEVENT_HUBERT_CHAN
from .test_client import IRCEVENT_HUBERT_PRIV
from .test_client import IRCEVENT_RANDOM_CHAN
from .test_client import IRCEVENT_RANDOM_PRIV



__all__ = [
    'IRCEVENTS',
    'IRCEVENT_HUBERT_CHAN',
    'IRCEVENT_HUBERT_PRIV',
    'IRCEVENT_RANDOM_CHAN',
    'IRCEVENT_RANDOM_PRIV']



SAMPLES = (
    Path(__file__).parent
    / 'samples')
