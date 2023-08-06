import pytest

import numpy as np
from numpy.testing import assert_allclose
from rdkit import Chem as rdChem

from rdkit_utilities import rdmolfiles, rdmolops


def test_OrderByMapNumber():
    mol = rdmolfiles.MolFromSmiles("[C:3][C:2][O:1]")
    assert mol.GetAtomWithIdx(0).GetSymbol() == "C"

    reordered = rdmolops.OrderByMapNumber(mol, clearAtomMapNumbers=False)
    first = reordered.GetAtomWithIdx(0)
    assert first.GetSymbol() == "O"
    assert first.GetAtomMapNum() == 1

    reordered = rdmolops.OrderByMapNumber(mol, clearAtomMapNumbers=True)
    first = reordered.GetAtomWithIdx(0)
    assert first.GetSymbol() == "O"
    assert first.GetAtomMapNum() == 0


@pytest.mark.parametrize(
    "core_indices, include_central_atoms, n_neighbors, expected_indices",
    [
        ({14}, True, -1, set(range(25))),
        ({14}, False, -1, set(range(14)) | set(range(15, 25))),
        ({14}, True, 0, {14}),
        ({14}, False, 0, set()),
        ({14}, True, 1, {12, 14, 15}),
        ({14}, False, 1, {12, 15}),
        ({14}, True, 2, {7, 13, 12, 14, 15, 16, 17, 18}),
        ({14}, False, 2, {7, 13, 12, 15, 16, 17, 18}),
        ({14}, True, 3, {5, 8, 7, 13, 12, 14, 15, 16, 17, 18, 19, 20, 21}),
        ({14}, False, 3, {5, 8, 7, 13, 12, 15, 16, 17, 18, 19, 20, 21}),
        ({2, 12, 21}, True, -1, set(range(25))),
        ({2, 12, 21}, True, 0, {2, 12, 21}),
        ({2, 12, 21}, False, 0, set()),
        ({2, 12, 21}, False, 1, {1, 3, 10, 7, 13, 14, 18, 22, 23, 24}),
        ({2, 12}, False, 2, {0, 1, 3, 4, 5, 10, 8, 11, 7, 13, 14, 5, 8, 15}),
    ],
)
def test_GetAtomNeighborIndices(
    propylparaben, core_indices, include_central_atoms, n_neighbors, expected_indices
):
    indices = rdmolops.GetAtomNeighborIndices(
        propylparaben,
        centralAtomIndices=core_indices,
        includeCentralAtoms=include_central_atoms,
        numAtomNeighbors=n_neighbors,
    )
    assert indices == expected_indices


@pytest.fixture()
def mol_with_conformers():
    from rdkit_utilities.rdchem import AddConformerWithCoordinates

    mol = rdmolfiles.MolFromSmarts("[O]=[C]=[O]")
    coords = np.zeros((3, 3), dtype=float)
    for i in range(10):
        AddConformerWithCoordinates(mol, coords + i)
    return mol


def test_ReorderConformers(mol_with_conformers):
    conf = mol_with_conformers.GetConformer(0)
    assert_allclose(np.array(conf.GetPositions())[0], [0, 0, 0])
    assert conf.GetId() == 0

    order = [4, 2, 1, 0, 3, 5, 6, 7, 8, 9]
    rdmolops.ReorderConformers(mol_with_conformers, order)
    conf = mol_with_conformers.GetConformer(0)
    assert_allclose(np.array(conf.GetPositions())[0], [4, 4, 4])
    assert conf.GetId() == 0


def test_KeepConformerIds(mol_with_conformers):
    rdmolops.KeepConformerIds(mol_with_conformers, [1, 0, 3, 5, 6, 7])
    conformer_ids = [conf.GetId() for conf in mol_with_conformers.GetConformers()]
    assert conformer_ids == [0, 1, 3, 5, 6, 7]


@pytest.mark.parametrize(
    "atom_indices_in, atom_nums_out",
    [([], []), ([0, 1], [1, 2]), ([5, 0, 3, 2], [1, 3, 4]), ((3, 4, 4), [4, 5])],
)
def test_SubsetMol(methane, atom_indices_in, atom_nums_out):
    subset = rdmolops.SubsetMol(methane, atom_indices_in)
    assert methane.GetNumAtoms() == 5

    subset_nums = [atom.GetAtomMapNum() for atom in subset.GetAtoms()]
    assert subset_nums == atom_nums_out


def test_MolToMolWithAtoms():
    query = rdmolfiles.MolFromSmarts("[*&r5]-[c:3]")
    assert all(isinstance(a, rdChem.QueryAtom) for a in query.GetAtoms())
    for atom in query.GetAtoms():
        atom.SetIsotope(10)
    last = query.GetAtomWithIdx(1)
    last.SetAtomMapNum(5)
    last.SetProp("dummy", "foo")

    mol = rdmolops.MolToMolWithAtoms(query)
    assert all(isinstance(a, rdChem.Atom) for a in mol.GetAtoms())

    assert mol.GetNumAtoms() == 2
    at1, at2 = list(mol.GetAtoms())
    q1, q2 = list(query.GetAtoms())

    assert q1.GetAtomicNum() == 0
    assert q1.GetSymbol() == "*"
    assert not q1.IsInRing()  # shouldn't show up in mol
    assert not q1.GetIsAromatic()
    assert not q1.GetAtomMapNum()
    assert q1.GetIsotope() == 10
    assert q1.GetSmarts() == "[r5]"

    assert at1.GetAtomicNum() == 0
    assert at1.GetSymbol() == "*"
    assert not at1.IsInRing()  # shouldn't show up in mol
    assert not at1.GetIsAromatic()
    assert not at1.GetAtomMapNum()
    assert at1.GetIsotope() == 10

    assert q2.GetAtomicNum() == 6
    assert q2.GetSymbol() == "C"
    assert q2.GetIsAromatic()
    assert q2.GetAtomMapNum() == 5
    assert q2.GetIsotope() == 10

    assert at2.GetAtomicNum() == 6
    assert at2.GetSymbol() == "C"
    assert at2.GetIsAromatic()
    assert at2.GetAtomMapNum() == 5
    assert at2.GetIsotope() == 10
    assert at2.GetProp("dummy") == "foo"

    assert rdChem.MolToSmarts(query) == "[r5]-[c:5]"
    assert rdChem.MolToSmarts(mol) == "[10#0]-[10#6:5]"

    return_trip = rdmolops.MolToMolWithQueryAtoms(mol)
    assert rdChem.MolToSmarts(return_trip) == "[r5&10*]-[c&10*:5]"


@pytest.mark.parametrize(
    "strict, includeIsotopes, smarts",
    [
        # Atom.GetSmarts contains isotopes even though QueryAtom.GetSmarts does not
        (False, False, "[C&H1](=[O&4*])-[O&-]"),
        (False, True, "[C&H1](=[O&4*])-[O&-]"),
        (True, True, "[C&H1&0*](=[O&4*])-[O&-&0*]"),
    ],
)
def test_MolToMolWithQueryAtoms_from_smiles(strict, includeIsotopes, smarts):
    mol = rdChem.MolFromSmiles("C(=[4O])-[O-]")
    assert mol.GetNumAtoms() == 3
    at1, at2, at3 = list(mol.GetAtoms())
    assert at2.GetIsotope() == 4
    assert at2.GetSmarts() == "[4O]"
    assert at3.GetIsotope() == 0
    at1.SetProp("dummy", "foo")

    query = rdmolops.MolToMolWithQueryAtoms(
        mol, strict=strict, includeIsotopes=includeIsotopes
    )
    assert query.GetAtomWithIdx(0).GetProp("dummy") == "foo"
    output_smarts = rdChem.MolToSmarts(query)
    assert output_smarts == smarts


@pytest.mark.parametrize(
    "strict, includeIsotopes, smarts",
    [
        # Atom.GetSmarts contains isotopes even though QueryAtom.GetSmarts does not
        (False, False, "C(=O)-[O&-:5]"),
        (False, True, "C(=[O&4*])-[O&-:5]"),
        (True, True, "[C&0*](=[O&4*])-[O&-&0*:5]"),
    ],
)
def test_MolToMolWithQueryAtoms_from_smarts(strict, includeIsotopes, smarts):
    mol = rdChem.MolFromSmarts("C(=[O])-[O-]")
    assert mol.GetNumAtoms() == 3
    at1, at2, at3 = list(mol.GetAtoms())
    assert at1.GetSmarts() == "C"
    at2.SetIsotope(4)
    assert at2.GetSmarts() == "O"
    at3.SetAtomMapNum(5)
    assert at3.GetSmarts() == "[O&-:5]"

    query = rdmolops.MolToMolWithQueryAtoms(
        mol, strict=strict, includeIsotopes=includeIsotopes
    )
    output_smarts = rdChem.MolToSmarts(query)
    assert output_smarts == smarts

    normal_mol = rdmolops.MolToMolWithAtoms(mol)
    query_from_normal = rdmolops.MolToMolWithQueryAtoms(
        normal_mol, strict=strict, includeIsotopes=includeIsotopes
    )
    output_smarts_from_normal = rdChem.MolToSmarts(query_from_normal)
    assert output_smarts_from_normal == smarts


def test_MolToMolIdentity():
    smiles = rdChem.MolFromSmiles("CC")
    smiles_to_smiles = rdmolops.MolAsMolWithAtoms(smiles)
    assert smiles_to_smiles is smiles

    smiles_to_smarts = rdmolops.MolAsMolWithQueryAtoms(smiles)
    assert smiles_to_smarts is not smiles
    assert rdChem.MolToSmarts(smiles_to_smarts) == "[C&H3]-[C&H3]"

    smarts = rdChem.MolFromSmarts("CC")
    smarts_to_smiles = rdmolops.MolAsMolWithAtoms(smarts)
    assert smarts_to_smiles is not smarts
    assert rdChem.MolToSmarts(smarts) == "CC"

    smarts_to_smarts = rdmolops.MolAsMolWithQueryAtoms(smarts)
    assert smarts_to_smarts is smarts
