import pytest
import numpy as np

from rdkit import Chem as rdChem
from rdkit_utilities import rdmolops, rdmolfiles, rdchem


@pytest.fixture
def propylparaben():
    rdmol = rdmolfiles.MolFromSmiles(
        (
            "[H:1]-[O:2]-[c:3]1:[c:4](-[H:5]):[c:6](-[H:7])"
            ":[c:8](-[C:13](=[O:14])-[O:15]-[C:16](-[H:17])"
            "(-[H:18])-[C:19](-[H:20])(-[H:21])-[C:22](-[H:23])"
            "(-[H:24])-[H:25]):[c:9](-[H:10]):[c:11]:1-[H:12]"
        ),
        removeHs=False,
    )
    rdmol = rdmolops.OrderByMapNumber(rdmol, clearAtomMapNumbers=True)
    return rdmol


@pytest.fixture
def methane():
    mol = rdmolfiles.MolFromSmarts(
        "[H:2]-[C:1](-[H:3])(-[H:4])-[H:5]",
        orderByMapNumber=True,
    )
    for i in range(5):
        conf = np.ones((5, 3), dtype=float) * np.arange(5).reshape((5, 1))
        conf[i] += 10
        rdchem.AddConformerWithCoordinates(mol, conf)
    rdChem.SanitizeMol(mol)
    return mol


@pytest.fixture()
def ethane():
    from rdkit.Chem import AllChem

    mol = rdmolfiles.MolFromSmiles("CC")
    mol = rdChem.AddHs(mol)
    rdChem.SanitizeMol(mol)
    AllChem.EmbedMolecule(mol)
    return mol
