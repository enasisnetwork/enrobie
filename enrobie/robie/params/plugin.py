"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from .child import RobieChildParams



class RobiePluginParams(RobieChildParams, extra='forbid'):
    """
    Process and validate the Robie configuration parameters.
    """
