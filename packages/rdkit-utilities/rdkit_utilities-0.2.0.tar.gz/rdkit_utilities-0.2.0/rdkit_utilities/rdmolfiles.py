"""
rdkit_utilities.py
RDKit utilities

"""
from typing import Optional, Dict
from typing_extensions import Literal

from rdkit import Chem as rdChem

from ._io._rdmolfiles import *
from ._io._parser import ALL_RDKIT_PARSERS, molecule_from_input


@reorder_constructed_molecule
def MolFromInput(
    molInput: str,
    *args,
    inputFormat: Optional[Literal[(*ALL_RDKIT_PARSERS,)]] = None,  # type: ignore
    orderByMapNumber: bool = False,
    clearAtomMapNumbers: bool = False,
    **kwargs,
) -> Optional[rdChem.Mol]:
    """Construct RDKit Mol from input with optional format.

    This accepts any input that RDKit can parse, and looks for the
    appropriate function to load the data.

    Parameters
    ----------
    molInput: str
        Molecule data or filename
    *args
        Passed to the RDKit parsing function
    inputFormat
        Format of `molInput`. If not given, it's guessed from
        the extension of the filename, or all of RDKit's content
        parsers are tried one-by-one.
    orderByMapNumber: bool
        Whether to reorder the molecule by atom map number
    clearAtomMapNumbers: bool
        Whether to remove / set all atom map numbers to 0
    """
    return molecule_from_input(molInput, *args, mol_format=inputFormat, **kwargs)
