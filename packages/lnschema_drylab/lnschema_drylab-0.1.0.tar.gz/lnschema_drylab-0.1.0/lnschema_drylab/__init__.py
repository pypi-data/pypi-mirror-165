"""Schema module drylab (`xqfj`).

Import the package::

   import lnschema_drylab

Main tables:

.. autosummary::
   :toctree: .

   environment

Tracking migrations:

.. autosummary::
   :toctree: .

   version_xqfj

Auxiliary modules:

.. autosummary::
   :toctree: .

   type
   id

"""
# This is lnschema-module xqfj.
_schema_module_id = "xqfj"
__version__ = "0.1.0"  # denote a pre-release for 0.1.0 with 0.1a1

from . import id, type  # noqa
from ._core import environment, version_xqfj  # noqa
