"""
This is a bit of a hacky way to override RDKit functions
"""
import os
from typing import Optional

from rdkit.Chem.rdmolfiles import *  # type: ignore
from rdkit_utilities._io._rdmolfiles import *

CONTENT_PARSERS = {
    "fasta": MolFromFASTA,
    "helm": MolFromHELM,
    "mol": MolFromMolBlock,
    "mol2": MolFromMol2Block,
    "pdb": MolFromPDBBlock,
    "png": MolFromPNGString,
    "svg": MolFromRDKitSVG,
    "sequence": MolFromSequence,
    "seq": MolFromSequence,
    "smarts": MolFromSmarts,
    "smiles": MolFromSmiles,
    "tpl": MolFromTPLBlock,
}

FILE_PARSERS = {
    "mol": MolFromMolFile,
    "mol2": MolFromMol2File,
    "pdb": MolFromPDBFile,
    "png": MolFromPNGFile,
    "tpl": MolFromTPLFile,
}

ALL_RDKIT_PARSERS = sorted(set(CONTENT_PARSERS) | set(FILE_PARSERS))


def molecule_from_input(mol_input, *args, mol_format: Optional[str] = None, **kwargs):
    if os.path.isfile(mol_input):
        content_reader = FILE_PARSERS
        if not mol_format:
            mol_format = os.path.splitext(mol_input)[1][1:]
    else:
        content_reader = CONTENT_PARSERS
    if mol_format:
        try:
            reader = content_reader[mol_format.lower()]
        except KeyError:
            raise TypeError(
                f"Molecule format {mol_format} not supported. "
                f"Supported formats: " + ", ".join(ALL_RDKIT_PARSERS)
            )
        return reader(mol_input, *args, **kwargs)

    for reader in content_reader.values():
        try:
            mol = reader(mol_input, *args, **kwargs)
        except RuntimeError:
            pass
        else:
            if mol is not None:
                return mol

    raise TypeError(
        f"Could not create an RDKit molecule from {mol_input}. "
        "Try passing in a `mol_format`. "
        f"Supported formats: " + ", ".join(ALL_RDKIT_PARSERS)
    )
