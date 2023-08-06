"""
Functions to do with molecules that are analogous to rdkit.Chem.rdchem.
"""

from typing import List, Tuple, Union, Dict, Any

from rdkit import Chem as rdChem
import numpy as np

from .utils import isiterable


def AddConformerWithCoordinates(
    mol: rdChem.Mol,
    coordinates: np.ndarray,
) -> int:
    """Add conformer to molecule with coordinates in angstrom"""
    from rdkit import Geometry

    n_atoms = mol.GetNumAtoms()
    coord_type = np.asarray(coordinates)
    if coord_type.shape != (n_atoms, 3):
        raise ValueError(
            f"Shape of coordinates must be ({n_atoms}, 3). "
            f"Given array with shape {coord_type.shape}"
        )
    conformer = rdChem.Conformer(n_atoms)
    for i, xyz in enumerate(coordinates):
        x, y, z = map(float, xyz)
        conformer.SetAtomPosition(i, Geometry.Point3D(x, y, z))
    conformer.SetId(mol.GetNumConformers())
    return mol.AddConformer(conformer)


def GetSymmetricAtomIndices(
    mol: rdChem.Mol,
    maxMatches: int = 10000,
) -> List[Tuple[int, ...]]:
    """Get atom indices of symmetric atoms

    Returns
    -------
    symmetric_indices: List[Tuple[int, ...]]
        In this list, one item is a sorted tuple of indices,
        where each index indicates an atom that is symmetric
        to all the other indices in the tuple.
    """
    # take care of resonance
    matches = [
        match
        for resMol in rdChem.ResonanceMolSupplier(mol)
        for match in resMol.GetSubstructMatches(
            mol, uniquify=False, maxMatches=maxMatches
        )
    ]
    atom_symmetries = set(tuple(sorted(set(x))) for x in zip(*matches))
    return sorted([x for x in atom_symmetries if len(x) > 1])


def GetTaggedSubstructMatches(
    mol: rdChem.Mol,
    query: rdChem.Mol,
    uniquify: bool = False,
    useChirality: bool = False,
    useQueryQueryMatches: bool = False,
    maxMatches: int = 1000,
    mappingAsTaggedDict: bool = False,
) -> Union[List[Tuple[int, ...]], List[Dict[int, int]]]:
    """Only return tagged atoms in substruct match, in tag order"""
    matches = mol.GetSubstructMatches(
        query,
        uniquify=uniquify,
        useChirality=useChirality,
        useQueryQueryMatches=useQueryQueryMatches,
        maxMatches=maxMatches,
    )
    map_numbers = np.array([a.GetAtomMapNum() for a in query.GetAtoms()])
    not_zero = np.where(map_numbers)[0]
    matches = [
        tuple(x for i, x in enumerate(match) if i in not_zero) for match in matches
    ]
    matches = sorted(set(matches))
    map_numbers = map_numbers[not_zero]
    order = np.argsort(map_numbers)
    matches = [tuple(match[i] for i in order) for match in matches]
    if mappingAsTaggedDict:
        map_numbers = list(map(int, map_numbers[order]))
        return [dict(zip(map_numbers, match)) for match in matches]
    return matches


def SetPropsFromDict(obj: Union[rdChem.Mol, rdChem.Atom], properties: Dict[str, Any]):
    """Set properties from dict, analogous to GetPropsAsDict()"""
    for key, val in properties.items():
        if key == "__computedProps":
            continue
        valtype = type(val)
        if val is False or val is True or np.issubdtype(valtype, np.bool_):
            obj.SetBoolProp(key, bool(val))
        # exhaustively list np types for Windows
        elif (isinstance(val, (int, np.int_, np.int16, np.int32, np.int64, np.int0, np.intp, np.intc))
            or np.issubdtype(valtype, np.int_)):
            obj.SetIntProp(key, int(val))
        elif (isinstance(val, (float, np.float_, np.float16, np.float32, np.float64))
            or np.issubdtype(valtype, np.float_)):
            obj.SetDoubleProp(key, float(val))
        elif isinstance(val, str) or np.issubdtype(valtype, str):
            obj.SetProp(key, val)
        elif isinstance(val, rdChem.rdBase._vecti):
            obj.SetExplicitBitVectProp(key, val)
        else:
            raise ValueError(f"No setter function for {val} of type {valtype}")
