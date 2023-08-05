"""Bio file readers, instrument schema.

Import the package::

   import bioreadout

This is the complete API reference:

.. autosummary::
   :toctree: .

   readout
"""

__version__ = "0.1.0"

from . import lookup  # noqa
from ._efo import EFO, readout  # noqa
