"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from .test_client import MTMEVENTS
from .test_client import MTMEVENT_HUBERT_CHAN
from .test_client import MTMEVENT_HUBERT_PRIV
from .test_client import MTMEVENT_RANDOM_CHAN
from .test_client import MTMEVENT_RANDOM_PRIV



__all__ = [
    'MTMEVENTS',
    'MTMEVENT_HUBERT_CHAN',
    'MTMEVENT_HUBERT_PRIV',
    'MTMEVENT_RANDOM_CHAN',
    'MTMEVENT_RANDOM_PRIV']



SAMPLES = (
    Path(__file__).parent
    / 'samples')
