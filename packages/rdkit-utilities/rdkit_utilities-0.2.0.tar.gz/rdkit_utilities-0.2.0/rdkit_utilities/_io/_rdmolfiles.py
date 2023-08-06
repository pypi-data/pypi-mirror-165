import functools
from typing import Optional, Dict

from rdkit import Chem as rdChem


__all__ = [
    "reorder_constructed_molecule",
    "MolFromSmiles",
    "MolFromSmarts",
]


def reorder_constructed_molecule(func):
    @functools.wraps(func)
    def wrapper(
        *args,
        orderByMapNumber: bool = False,
        clearAtomMapNumbers: bool = False,
        **kwargs
    ):
        mol = func(*args, **kwargs)
        if orderByMapNumber and mol is not None:
            from rdkit_utilities.rdmolops import OrderByMapNumber

            mol = OrderByMapNumber(mol, clearAtomMapNumbers=clearAtomMapNumbers)
        elif clearAtomMapNumbers:
            for atom in mol.GetAtoms():
                atom.SetAtomMapNum(0)
        return mol

    return wrapper


@reorder_constructed_molecule
def MolFromSmiles(
    smiles: str,
    allowCXSMILES: bool = True,
    maxIterations: int = 0,
    parseName: bool = False,
    removeHs: bool = True,
    sanitize: bool = True,
    strictCXSMILES: bool = True,
    useLegacyStereo: bool = True,
    orderByMapNumber: bool = False,
    clearAtomMapNumbers: bool = False,
) -> Optional[rdChem.Mol]:
    """
    Create a molecule from a SMILES string.

    Parameters
    ----------
    smiles: str
    orderByMapNumber: bool
        Whether to reorder the molecule by atom map number
    clearAtomMapNumbers: bool
        Whether to remove / set all atom map numbers to 0
    **kwargs
        Passed to rdkit.Chem.SmilesParserParams

    Example
    -------

    ::

        >>> rdmol = MolFromSmiles("[C:3][C:2][H:1]")
        >>> rdmol.GetNumAtoms()
        2
        >>> rdmol = MolFromSmiles("[C:3][C:2][H:1]", removeHs=False)
        >>> rdmol.GetNumAtoms()
        3
    """
    smiles_parser = rdChem.rdmolfiles.SmilesParserParams()
    smiles_parser.allowCXSMILES = allowCXSMILES
    smiles_parser.maxIterations = maxIterations
    smiles_parser.parseName = parseName
    smiles_parser.removeHs = removeHs
    smiles_parser.sanitize = sanitize
    smiles_parser.strictCXSMILES = strictCXSMILES
    smiles_parser.useLegacyStereo = useLegacyStereo
    mol = rdChem.MolFromSmiles(smiles, smiles_parser)
    return mol


@reorder_constructed_molecule
def MolFromSmarts(
    smarts: str,
    mergeHs: bool = False,
    replacements: Dict[str, str] = {},
    asQueryAtoms: bool = True,
    orderByMapNumber: bool = False,
    clearAtomMapNumbers: bool = False,
) -> Optional[rdChem.Mol]:
    """
    Create a molecule from a SMARTS string.

    Parameters
    ----------
    smarts: str
    orderByMapNumber: bool
        Whether to reorder the molecule by atom map number
    clearAtomMapNumbers: bool
        Whether to remove / set all atom map numbers to 0
    **kwargs
        Passed to rdkit.Chem.SmilesParserParams

    """
    mol = rdChem.MolFromSmarts(smarts, mergeHs=mergeHs, replacements=replacements)
    if not asQueryAtoms and mol is not None:
        from ..rdmolops import MolToMolWithAtoms

        return MolToMolWithAtoms(mol)
    return mol
