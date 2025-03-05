"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from importlib import import_module
from typing import Any



def importer(
    path: str,
) -> Any:  # noqa: ANN401
    """
    Return the function or class using the importable path.

    :param path: Importable Python path for the operation.
    :returns: Function or class using the importable path.
    """

    root, name = (
        path.rsplit('.', 1))

    module = import_module(root)

    return getattr(module, name)
