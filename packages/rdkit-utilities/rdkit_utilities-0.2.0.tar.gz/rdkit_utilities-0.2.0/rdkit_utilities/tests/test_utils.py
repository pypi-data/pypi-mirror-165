import pytest

import numpy as np
from numpy.testing import assert_allclose


def test_compute_distance_matrix():
    from rdkit_utilities import utils

    arr = np.arange(24).reshape((2, 4, 3))
    rms = utils.compute_atom_distance_matrix(arr)
    assert rms.shape == (2, 4, 4)

    first_row = [0, 5.19615242, 10.39230485, 15.58845727]
    assert_allclose(rms[0, 0], first_row)
    assert_allclose(rms[-1, 0], first_row)

    last_row = [15.58845727, 10.39230485, 5.19615242, 0]
    assert_allclose(rms[0, -1], last_row)
    assert_allclose(rms[-1, -1], last_row)


@pytest.mark.parametrize(
    "threshold, n_indices, indices",
    [
        (0.05, 4, [0, 3, 1, 2]),
        (0.05, 10, [0, 3, 1, 2]),
        (0.05, 2, [0, 3]),
        (10, 4, [0, 3]),
        (5.4, 4, [0, 3, 1]),
    ],
)
def test_get_maximally_diverse_indices(threshold, n_indices, indices):
    from rdkit_utilities import utils

    arr = np.array(
        [
            [0.0, 5.49615242, 10.39230485, 15.58845727],
            [5.49615242, 0.0, 5.19615242, 10.39230485],
            [10.39230485, 5.19615242, 0.0, 5.19615242],
            [15.58845727, 10.39230485, 5.19615242, 0.0],
        ]
    )
    computed = utils.get_maximally_diverse_indices(
        arr,
        distance_threshold=threshold,
        n_indices=n_indices,
    )
    assert computed == indices
