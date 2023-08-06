import itertools
from typing import Optional, List

from rdkit import Chem as rdChem
import numpy as np


def GetBestConformerRMS(
    mol: rdChem.Mol, heavyAtomsOnly: bool = False, confIds: Optional[List[int]] = None
) -> np.ndarray:
    """Get square array of conformer-to-conformer symmetric RMS

    Parameters
    ----------
    mol: rdkit.Chem.Mol
        Molecule of interest
    heavyAtomsOnly: bool
        If True, all hydrogens are removed before calculating RMS.
        This is done on a copy to avoid changing the molecule
    confIds: Optional[List[int]]
        If given, the RMS calculation is limited to these conformer IDs.
        If not, all conformers are used.

    Returns
    -------
    rms: numpy.ndarray
        Square array of RMS from each conformer to each other.
        This is ordered by the input `confIds` if given, or
        by the order of the conformers on the molecule if `confIds=None`.
    """
    from rdkit.Chem import rdMolAlign

    if confIds is None:
        confIds = [c.GetId() for c in mol.GetConformers()]
    n_conformers = len(confIds)

    if heavyAtomsOnly:
        mol = rdChem.RemoveAllHs(mol, sanitize=False)
        rdChem.SanitizeMol(
            mol,
            rdChem.SANITIZE_ALL
            ^ rdChem.SANITIZE_SETAROMATICITY
            ^ rdChem.SANITIZE_SETCONJUGATION
            ^ rdChem.SANITIZE_SETHYBRIDIZATION
            ^ rdChem.SANITIZE_ADJUSTHS,
        )

    rms = np.zeros((n_conformers, n_conformers))
    for i, j in itertools.combinations(np.arange(n_conformers), 2):
        rmsd = rdMolAlign.GetBestRMS(mol, mol, confIds[i], confIds[j])
        rms[i, j] = rms[j, i] = rmsd
    return rms
