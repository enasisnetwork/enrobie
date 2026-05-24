"""
Functions and routines associated with Enasis Network Chatting Robie.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""
# pylint: disable=import-error



from pathlib import Path
from sys import path as sys_path
from typing import Any

from sphinx.application import Sphinx



SPHINX = (
    Path(__file__).parent
    .resolve())

PARENT = (
    SPHINX.parent
    .as_posix())

sys_path.insert(
    0, PARENT)

from enrobie import BOILER
from enrobie import VERSION



project = 'enrobie'
copyright = '2026, Enasis Network'
author = 'Enasis Network'
nitpicky = True
version = VERSION

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'sphinxcontrib.pydantic']

html_static_path = ['_static']
html_theme = 'pydata_sphinx_theme'
html_favicon = '_static/icon.png'

autodoc_member_order = 'bysource'

always_document_param_types = True

intersphinx_mapping = {
    'encommon': ('https://enasisnetwork.github.io/encommon/sphinx', None),
    'enconnect': ('https://enasisnetwork.github.io/enconnect/sphinx', None),
    'enhomie': ('https://enasisnetwork.github.io/enhomie/sphinx', None),
    'pydantic': ('https://docs.pydantic.dev/latest', None),
    'pytest': ('https://docs.pytest.org/latest', None),
    'python': ('https://docs.python.org/3', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master', None)}



def boilerplate(
    app: Sphinx,
    what: str,
    name: str,
    obj: Any,  # noqa: ANN401
    options: Any,  # noqa: ANN401
    lines: list[str],
) -> None:
    """
    Remove the boilerplate header from each of the modules.
    """

    if what != 'module':
        return None

    length = len(BOILER)

    text = lines[:length]

    if text == BOILER:
        del lines[:length]



def setup(
    app: Sphinx,
) -> None:
    """
    Perform extra setup when called on by Sphinx processes.
    """

    app.add_css_file('style.css')

    app.connect(
        'autodoc-process-docstring',
        boilerplate)
