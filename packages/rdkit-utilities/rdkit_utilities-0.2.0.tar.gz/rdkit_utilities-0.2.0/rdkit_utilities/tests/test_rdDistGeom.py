import pytest

import numpy as np
from numpy.testing import assert_allclose

from rdkit_utilities import rdmolfiles, rdchem, rdDistGeom
from rdkit import Chem as rdChem


@pytest.fixture
def formic_acid():
    mol = rdmolfiles.MolFromSmiles(
        "[H:4][C:2](=[O:1])[O:3][H:5]",
        orderByMapNumber=True,
        removeHs=False,
        clearAtomMapNumbers=True,
    )
    return mol


def test_SelectDiverseELFConformers():
    smiles = "[H:6]/[C:1](=[C:2](\\[H:7])/[O:3][H:8])/[C:4](=[O:5])[H:9]"
    mol = rdmolfiles.MolFromSmiles(smiles, orderByMapNumber=True, removeHs=False)
    conformers = np.array(
        [
            [
                [0.5477, 0.3297, -0.0621],
                [-0.1168, -0.7881, 0.2329],
                [-1.4803, -0.8771, 0.1667],
                [-0.2158, 1.5206, -0.4772],
                [-1.4382, 1.5111, -0.5580],
                [1.6274, 0.3962, -0.0089],
                [0.3388, -1.7170, 0.5467],
                [-1.8612, -0.0347, -0.1160],
                [0.3747, 2.4222, -0.7115],
            ],
            [
                [0.5477, 0.3297, -0.0621],
                [-0.1168, -0.7881, 0.2329],
                [-1.4803, -0.8771, 0.1667],
                [-0.2158, 1.5206, -0.4772],
                [0.3353, 2.5772, -0.7614],
                [1.6274, 0.3962, -0.0089],
                [0.3388, -1.7170, 0.5467],
                [-1.7743, -1.7634, 0.4166],
                [-1.3122, 1.4082, -0.5180],
            ],
        ]
    )
    for conf in conformers:
        rdchem.AddConformerWithCoordinates(mol, conf)
    assert mol.GetNumConformers() == 2

    rdDistGeom.SelectDiverseELFConformers(mol)
    assert mol.GetNumConformers() == 1

    selected = np.array(mol.GetConformer(0).GetPositions())
    assert_allclose(selected, conformers[1])


def test_RemoveTransAcidConformers(formic_acid):
    cis = np.array(
        [
            [-0.95927322, -0.91789997, 0.36333418],
            [-0.34727824, 0.12828046, 0.22784603],
            [0.82766682, 0.26871252, -0.42284882],
            [-0.67153811, 1.10376000, 0.61921501],
            [1.15035689, -0.58282924, -0.78766006],
        ]
    )
    trans = np.array(
        [
            [-0.95927322, -0.91789997, 0.36333418],
            [-0.34727824, 0.12828046, 0.22784603],
            [0.82766682, 0.26871252, -0.42284882],
            [-0.67153811, 1.10376000, 0.61921501],
            [1.14532626, 1.19679034, -0.41266876],
        ]
    )
    rdchem.AddConformerWithCoordinates(formic_acid, cis)
    rdchem.AddConformerWithCoordinates(formic_acid, trans)

    assert formic_acid.GetNumConformers() == 2
    rdDistGeom.RemoveTransAcidConformers(formic_acid)
    assert formic_acid.GetNumConformers() == 1

    coordinates = np.array(formic_acid.GetConformer(0).GetPositions())
    assert_allclose(coordinates, cis)


def test_CalculateElectrostaticEnergy(formic_acid):
    assert formic_acid.GetNumConformers() == 0

    dummy1 = np.array(
        [
            [1.0, 0.0, 0.0],  # =O
            [0.0, 0.0, 0.0],  # C
            [-1.0, 0.0, 0.0],  # -O-
            [0.0, 1.0, 0.0],  # H-(C)
            [0.0, -1.0, 0.0],  # H-(O)
        ]
    )

    # swap O
    dummy2 = np.array(
        [
            [-1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
        ]
    )

    # swap H
    dummy3 = np.array(
        [
            [-1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 1.0, 0.0],
        ]
    )

    # shake it up
    dummy4 = np.array(
        [
            [-1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [1.0, 0.0, 0.0],
        ]
    )

    rdchem.AddConformerWithCoordinates(formic_acid, dummy1)
    rdchem.AddConformerWithCoordinates(formic_acid, dummy2)
    rdchem.AddConformerWithCoordinates(formic_acid, dummy3)
    rdchem.AddConformerWithCoordinates(formic_acid, dummy4)
    assert formic_acid.GetNumConformers() == 4

    energies = rdDistGeom.CalculateElectrostaticEnergy(formic_acid)
    assert energies.shape == (4,)
    desired_energies = [0.216525, 0.216525, 0.216525, 0.163713]
    assert_allclose(energies, desired_energies, atol=1e-6)


def test_GenerateConformers(formic_acid):
    assert formic_acid.GetNumConformers() == 0
    rdDistGeom.GenerateConformers(formic_acid, randomSeed=1)
    assert formic_acid.GetNumConformers() == 10

    lowest = formic_acid.GetConformer(0)
    coordinates = np.array(lowest.GetPositions())
    first_coord = [-0.677714, 1.017283, 0.609685]
    assert_allclose(coordinates[0], first_coord, atol=1e-6)


@pytest.mark.parametrize(
    "numConfPool, maximizeDiversity, selectELFConfs, optimizeConfs, n_confs",
    [
        (None, False, False, False, 10),
        (200, False, False, False, 10),
        (200, False, True, False, 4),
        (1000, False, True, False, 10),  # 10 selected from 20
        (200, True, False, False, 10),
        (10000, True, True, True, 10),
    ],
)
def test_GenerateConformers_options(
    numConfPool, maximizeDiversity, selectELFConfs, optimizeConfs, n_confs
):
    mol = rdChem.AddHs(rdmolfiles.MolFromSmiles("CCCCCC"))
    rdDistGeom.GenerateConformers(
        mol,
        numConfPool=numConfPool,
        maximizeDiversity=maximizeDiversity,
        selectELFConfs=selectELFConfs,
        optimizeConfs=optimizeConfs,
        diverseRmsThresh=0.01,
    )
    assert mol.GetNumConformers() == n_confs
