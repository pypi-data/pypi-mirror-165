import pytest
from rdkit_utilities import rdmolfiles
from rdkit_utilities.tests.datafiles import CCH_PDB


@pytest.mark.parametrize(
    "smiles, n_heavy_atoms, n_all_atoms",
    [
        ("[C:3][C:2][H:1]", 2, 3),
    ],
)
def test_MolFromSmiles(smiles, n_heavy_atoms, n_all_atoms):
    heavy_mol = rdmolfiles.MolFromSmiles(smiles)
    assert heavy_mol.GetNumAtoms() == n_heavy_atoms
    all_mol = rdmolfiles.MolFromSmiles(smiles, removeHs=False)
    assert all_mol.GetNumAtoms() == n_all_atoms


@pytest.mark.parametrize(
    "orderByMapNumber, clearAtomMapNumbers, firstElement, firstNum",
    [
        (False, False, "C", 3),
        (False, True, "C", 0),
        (True, False, "H", 1),
        (True, True, "H", 0),
    ],
)
def test_MolFromSmarts(orderByMapNumber, clearAtomMapNumbers, firstElement, firstNum):
    rdmol = rdmolfiles.MolFromSmarts(
        "[C:3][C:2][H:1]",
        orderByMapNumber=orderByMapNumber,
        clearAtomMapNumbers=clearAtomMapNumbers,
    )
    first = rdmol.GetAtomWithIdx(0)
    assert first.GetSymbol() == firstElement
    assert first.GetAtomMapNum() == firstNum


@pytest.mark.parametrize(
    "mol_format, mol_input, order_atoms, map_number",
    [
        ("smiles", "[C:3][C:2][H:1]", True, 2),
        ("smiles", "[C:3][C:2][H:1]", False, 3),
        ("smarts", "[C:3][C:2][H:1]", True, 1),
        ("smarts", "[C:3][C:2][H:1]", False, 3),
        (None, "[C:3][C:2][H:1]", True, 1),
        (None, "[C:3][C:2][H:1]", False, 3),
        ("pdb", CCH_PDB, True, 0),
        ("pdb", CCH_PDB, False, 0),
        (None, CCH_PDB, True, 0),
        (None, CCH_PDB, False, 0),
    ],
)
def test_mol_from_input(mol_format, mol_input, order_atoms, map_number):
    rdmol = rdmolfiles.MolFromInput(
        mol_input, inputFormat=mol_format, orderByMapNumber=order_atoms
    )
    first = rdmol.GetAtomWithIdx(0)
    assert first.GetAtomMapNum() == map_number
