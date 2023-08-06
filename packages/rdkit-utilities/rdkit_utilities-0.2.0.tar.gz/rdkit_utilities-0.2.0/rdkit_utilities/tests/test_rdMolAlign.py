import numpy as np
from numpy.testing import assert_allclose

from rdkit_utilities import rdMolAlign


def test_GetBestConformerRMS(methane):

    aa_rms = rdMolAlign.GetBestConformerRMS(methane, heavyAtomsOnly=False)
    assert aa_rms.shape == (5, 5)
    first_row = [0.0, 4.38178, 5.25357, 6.09918, 6.928203]
    assert_allclose(aa_rms[0], first_row, atol=1e-6)
    assert_allclose(aa_rms[:, 0], first_row, atol=1e-6)

    cg_rms = rdMolAlign.GetBestConformerRMS(methane, heavyAtomsOnly=True)
    assert cg_rms.shape == (5, 5)
    assert_allclose(cg_rms, 0, atol=1e-6)
