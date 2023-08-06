import pytest

from numpy.testing import assert_allclose

from rdkit_utilities import rdForceFieldHelpers


@pytest.mark.parametrize(
    "ff_name, energy",
    [
        ("UFF", 192350.97617245736),
        ("uff", 192350.97617245736),
        ("mmff", 69616788.17478018),
        ("MMFF94", 69616788.17478018),
        ("MMFF94S", 69616788.17478018),
    ],
)
def test_GetMoleculeForceField(methane, ff_name, energy):
    ff = rdForceFieldHelpers.GetMoleculeForceField(methane, forcefield=ff_name)
    assert_allclose(ff.CalcEnergy(), energy)


@pytest.mark.parametrize("ff", ["uff", "MMFF", "mmff94s"])
def test_FFOptimizeMolecule(ethane, ff):
    success = rdForceFieldHelpers.FFOptimizeMolecule(ethane, ff)
    assert success == 0


@pytest.mark.parametrize("ff", ["uff", "MMFF", "mmff94s"])
def test_FFOptimizeMoleculeConfs(ethane, ff):
    success_energies = rdForceFieldHelpers.FFOptimizeMoleculeConfs(ethane, ff)
    for conf in success_energies:
        assert conf[0] == 0
