from typing import Optional, List, Any

import numpy as np


def compute_atom_distance_matrix(coordinates: np.ndarray) -> np.ndarray:
    """Compute atom-to-atom distance for each conformer

    Parameters
    ----------
    coordinates: numpy.ndarray
        3D matrix of coordinates, with shape (n_conformers, n_atoms, 3)

    Returns
    -------
    distances: numpy.ndarray
        3D matrix of distances, with shape (n_conformers, n_atoms, n_atoms)
    """
    dist_sq = np.einsum("ijk,ilk->ijl", coordinates, coordinates)
    diag = np.einsum("ijj->ij", dist_sq)
    a, b = diag.shape
    dist_sq += dist_sq - diag.reshape((a, 1, b)) - diag.reshape((a, b, 1))
    diag[:] = -0.0
    return np.sqrt(-dist_sq)


def get_maximally_diverse_indices(
    distance_matrix: np.ndarray,
    distance_threshold: float = 0.05,
    n_indices: Optional[int] = None,
) -> List[int]:
    """Greedily select maximally diverse indices from distance_matrix

    Parameters
    ----------
    distance_matrix: numpy.ndarray
        2D square distance matrix with shape (n_items, n_items)
    distance_threshold: float
        If any item is below this threshold to any other item,
        they are considered too similar and only one will be included
        in the output
    n_indices: int
        Number of items to output

    Returns
    -------
    indices: List[int]
        List of indices of maximally diverse items.
    """
    n_distances = len(distance_matrix)
    if distance_matrix.shape != (n_distances, n_distances):
        raise ValueError("`distance_matrix` should be square distance matrix")

    if n_indices is None:
        n_indices = n_distances
    n_indices = min(n_indices, n_distances)

    selected_indices = [0]
    for i in range(n_indices - 1):
        selected_rms = distance_matrix[selected_indices]
        any_too_close = np.any(selected_rms < distance_threshold, axis=0)
        if np.all(any_too_close):
            break

        rmsdist = np.where(any_too_close, -np.inf, selected_rms.sum(axis=0))
        selected_indices.append(rmsdist.argmax())

    return selected_indices

def isiterable(obj: Any) -> bool:
    if hasattr(obj, "__next__"):
        return True
    if hasattr(obj, "__iter__"):
        return True
    try:
        len(obj)
    except TypeError:
        pass
    else:
        return True
    return False