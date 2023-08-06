"""Connect to the hub from LaminDB.

Import the package::

   import lndb_hub

This is the complete API reference:

.. autosummary::
   :toctree: .

   hub
"""

__version__ = "0.5.4"  # denote a pre-release for 0.1.0 with 0.1a1

from ._hub import get_hub_with_authentication, hub  # noqa
