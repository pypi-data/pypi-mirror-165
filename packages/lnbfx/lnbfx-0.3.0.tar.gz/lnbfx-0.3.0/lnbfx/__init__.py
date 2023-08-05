"""Manage bioinformatics pipelines.

Import the package::

   import lnbfx

This is the complete API reference:

.. autosummary::
   :toctree: .

   BfxRun
"""

__version__ = "0.3.0"  # denote a pre-release for 0.1.0 with 0.1a1

from . import schema
from ._core import BfxRun, get_bfx_files_from_dir, parse_bfx_file_type  # noqa
