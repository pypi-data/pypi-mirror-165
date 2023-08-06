"""
rdkit_utilities
RDKit utilities
"""

try:
    from rdkit import Chem as _
except ImportError:
    raise ImportError(
        "rdkit is an required for the functionality in this package. "
        "Please install it with `conda install -c conda-forge rdkit`."
    )

from .rdchem import *
from .rdDistGeom import *
from .rdForceFieldHelpers import *
from .rdMolAlign import *
from .rdmolfiles import *
from .rdmolops import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
