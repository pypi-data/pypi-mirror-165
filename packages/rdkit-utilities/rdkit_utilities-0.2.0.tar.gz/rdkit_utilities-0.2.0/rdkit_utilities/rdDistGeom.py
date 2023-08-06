import itertools
from typing import Optional, Dict, List, Union, Set, Tuple
from typing_extensions import Literal

import numpy as np

from rdkit import Chem as rdChem
from rdkit.Chem import AllChem as rdAllChem

from rdkit_utilities import rdForceFieldHelpers


def GetExclusions(mol: rdChem.Mol) -> Set[Tuple[int, int]]:
    """Get exclusions with a molecule between atoms 2- and 3- sites away"""
    exclusions = set()
    for i, atom in enumerate(mol.GetAtoms()):
        partners = [b.GetOtherAtomIdx(i) for b in atom.GetBonds()]
        exclusions |= set(tuple(sorted([i, x])) for x in partners)
        exclusions |= set(itertools.combinations(sorted(partners), 2))
    return exclusions


def GenerateConformers(
    mol: rdChem.Mol,
    numConfs: int = 10,
    numConfPool: Optional[int] = None,
    maximizeDiversity: bool = False,
    selectELFConfs: bool = False,
    ELFPercentage: float = 2.0,
    pruneRmsThresh: float = -1.0,
    diverseRmsThresh: float = 0.05,
    energyWindow: float = -1.0,
    maxAttempts: int = 0,
    randomSeed: int = -1,
    clearConfs: bool = True,
    useRandomCoords: bool = False,
    boxSizeMult: float = 2.0,
    randNegEig: bool = True,
    numZeroFail: int = 1,
    coordMap: Dict[int, Union[np.ndarray, List[float]]] = {},
    forceTol: float = 0.001,
    ignoreSmoothingFailures: bool = False,
    enforceChirality: bool = True,
    numThreads: int = 1,
    useExpTorsionAnglePrefs: bool = True,
    useBasicKnowledge: bool = True,
    printExpTorsionAngles: bool = False,
    useSmallRingTorsions: bool = False,
    useMacrocycleTorsions: bool = False,
    ETversion: int = 1,
    optimizeConfs: bool = False,
    forcefield: rdForceFieldHelpers.RDKIT_FF_TYPE = "MMFF94",
    optMaxIters: int = 200,
    ffVdwThresh: float = 10.0,
    ffNonBondedThresh: float = 100,
    ffIgnoreInterfragInteractions: bool = True,
    removeTransAcidConformers: bool = True,
) -> List[int]:
    """
    Generate conformers on molecule in-place.

    Parameters
    ----------
    numConfs: int
        Max number of conformers to end up with
    numConfPool: Optional[int]
        Max number of conformers to initially generate,
        for ELF or RMS selection.
    maximizeDiversity: bool
        Whether to maximize diversity via heavy-atom RMS
    selectELFConfs: bool
        Whether to select conformers using the electrostatically
        least-interacting functional group (ELF) technique
    ELFPercentage: float
        % (out of 100) of conformers to keep from `numConfPool`
        when selecting ELF conformers
    pruneRmsThresh: float
        RMS threshold to keep conformers initially generated
        from `numConfPool`
    diverseRmsThresh: float
        Minimum RMS threshold for distinguishing conformers
        when selecting maximally diverse conformers
    energyWindow: float
        If positive, only conformers within this energy
        window as determined by `forcefield` will be kept.
    optimizeConfs: bool
        Whether to optimize conformers generated initially,
        prior to selecting ELF and RMS diverse conformers.
    forcefield: Literal["UFF", "MMFF94", "MMFF94S"]
        Which force field to use for optimizing conformers
        and calculating energies for `energyWindow`.
    optMaxIters: int
        Maximum iterations for optimization
    ffVdwThresh: float
        VdW threshold for optimization and calculating energies
        using force field
    ffNonBondedThresh: float
        Non-bonded threshold for optimization and calculating energies
        using force field
    ffIgnoreInterfragInteractions: bool
        If True, nonbonded terms between fragments will not be added
        to the forcefield.
    **kwargs:
        See the RDKit documentation for
        ``rdkit.Chem.rdDistGeom.EmbedMultipleConfs``
        for more.
    """
    from .rdmolops import KeepConformerIds

    if not numConfPool:
        numConfPool = numConfs
        if maximizeDiversity or energyWindow > 0:
            numConfPool *= 1000

    coordMap = {k: list(map(float, v)) for k, v in coordMap.items()}

    rdAllChem.EmbedMultipleConfs(
        mol,
        numConfs=numConfPool,
        maxAttempts=maxAttempts,
        randomSeed=randomSeed,
        clearConfs=clearConfs,
        useRandomCoords=useRandomCoords,
        boxSizeMult=boxSizeMult,
        randNegEig=randNegEig,
        numZeroFail=numZeroFail,
        pruneRmsThresh=pruneRmsThresh,
        coordMap=coordMap,
        forceTol=forceTol,
        ignoreSmoothingFailures=ignoreSmoothingFailures,
        enforceChirality=enforceChirality,
        numThreads=numThreads,
        useExpTorsionAnglePrefs=useExpTorsionAnglePrefs,
        useBasicKnowledge=useBasicKnowledge,
        printExpTorsionAngles=printExpTorsionAngles,
        useSmallRingTorsions=useSmallRingTorsions,
        useMacrocycleTorsions=useMacrocycleTorsions,
        ETversion=ETversion,
    )

    if optimizeConfs:
        rdForceFieldHelpers.FFOptimizeMoleculeConfs(
            mol,
            forcefield=forcefield,
            numThreads=numThreads,
            maxIters=optMaxIters,
            vdwThresh=ffVdwThresh,
            nonBondedThresh=ffNonBondedThresh,
            ignoreInterfragInteractions=ffIgnoreInterfragInteractions,
        )

    if energyWindow > 0:
        RemoveConformersOutsideEnergyWindow(
            mol,
            energyWindow=energyWindow,
            forcefield=forcefield,
            numThreads=numThreads,
            ffVdwThresh=ffVdwThresh,
            ffNonBondedThresh=ffNonBondedThresh,
            ffIgnoreInterfragInteractions=ffIgnoreInterfragInteractions,
        )

    if selectELFConfs:
        SelectELFConformers(
            mol,
            ELFPercentage=ELFPercentage,
            removeTransAcidConformers=removeTransAcidConformers,
        )

    if maximizeDiversity:
        SelectDiverseConformers(
            mol, numConfs=numConfs, diverseRmsThresh=diverseRmsThresh
        )

    conformer_ids = [conf.GetId() for conf in mol.GetConformers()]
    KeepConformerIds(mol, conformer_ids[:numConfs])
    return mol.GetNumConformers()


def RemoveTransAcidConformers(mol: rdChem.Mol):
    """Remove conformers from molecule if they contain a trans carboxylic acid"""
    from rdkit.Chem.rdMolTransforms import GetDihedralRad  # type: ignore[import]
    from rdkit_utilities import rdmolfiles
    from .rdmolops import KeepConformerIds

    query = rdmolfiles.MolFromSmarts(
        "[#6X3:2](=[#8:1])(-[#8X2H1:3]-[#1:4])",
        orderByMapNumber=True,
    )
    matches = mol.GetSubstructMatches(query, uniquify=False)
    to_keep = []
    for conformer in mol.GetConformers():
        for match in matches:
            angle = GetDihedralRad(conformer, *match)
            if angle > np.pi / 2.0:
                break
        else:
            to_keep.append(conformer.GetId())
    KeepConformerIds(mol, to_keep)


def SelectELFConformers(
    mol: rdChem.Mol, ELFPercentage: float = 2.0, removeTransAcidConformers: bool = True
):
    """Keep percentage of conformers, ranked by electrostatic energy, in-place.

    The other conformers are deleted.
    """
    from .rdmolops import KeepConformerIds

    if removeTransAcidConformers:
        RemoveTransAcidConformers(mol)

    SortConformersByElectrostaticInteraction(mol)
    goal = int(mol.GetNumConformers() * ELFPercentage / 100)
    n_keep = max(1, goal)
    conformer_ids = [c.GetId() for c in mol.GetConformers()]
    keep_ids = conformer_ids[:n_keep]
    KeepConformerIds(mol, keep_ids)


def SelectDiverseConformers(
    mol: rdChem.Mol,
    numConfs: int = 10,
    diverseRmsThresh: float = 0.05,
):
    """Select conformers for max diversity by RMS, in-place.

    This uses a greedy algorithm. Unselected conformers are deleted.
    """
    from .rdMolAlign import GetBestConformerRMS
    from .rdmolops import KeepConformerIds
    from .utils import get_maximally_diverse_indices

    rms_matrix = GetBestConformerRMS(mol, heavyAtomsOnly=True)
    diverse_indices = get_maximally_diverse_indices(
        rms_matrix, distance_threshold=diverseRmsThresh, n_indices=numConfs
    )
    conformer_ids = [conf.GetId() for conf in mol.GetConformers()]
    keep_ids = [conformer_ids[i] for i in diverse_indices]
    KeepConformerIds(mol, keep_ids)
    for i, conf in enumerate(mol.GetConformers()):
        conf.SetId(i)


def SelectDiverseELFConformers(
    mol: rdChem.Mol,
    numConfs: int = 10,
    ELFPercentage: float = 2.0,
    diverseRmsThresh: float = 0.05,
    removeTransAcidConformers: bool = True,
):
    """Select diverse conformers using the ELF technique, in-place.

    Other conformers are deleted from the molecule.
    """
    SelectELFConformers(
        mol,
        ELFPercentage=ELFPercentage,
        removeTransAcidConformers=removeTransAcidConformers,
    )
    SelectDiverseConformers(mol, numConfs=numConfs, diverseRmsThresh=diverseRmsThresh)


def SortConformersByEnergy(
    mol: rdChem.Mol,
    forcefield: rdForceFieldHelpers.RDKIT_FF_TYPE = "MMFF94",
    numThreads: int = 1,
    ffVdwThresh: float = 10.0,
    ffNonBondedThresh: float = 100,
    ffIgnoreInterfragInteractions: bool = True,
    reverse: bool = False,
) -> List[float]:
    """Sort conformers in-place on molecule by force field energy.

    Returns
    -------
    energies: List[float]

    Raises
    ------
    ValueError
        If the force field cannot calculate energies
    """
    from .rdmolops import ReorderConformers

    result = rdForceFieldHelpers.FFOptimizeMoleculeConfs(
        mol,
        forcefield=forcefield,
        numThreads=numThreads,
        maxIters=0,
        vdwThresh=ffVdwThresh,
        nonBondedThresh=ffNonBondedThresh,
        ignoreInterfragInteractions=ffIgnoreInterfragInteractions,
    )
    energies = [x[1] for x in result]
    if any(x == -1 for x in energies):
        raise ValueError(
            f"Could not use {forcefield} to calculate energies "
            f"for {rdChem.MolToSmarts(mol)}. "
            "Cannot sort conformers by energy."
        )
    order = np.argsort(energies)
    if reverse:
        order = order[::-1]
    ReorderConformers(mol, order)
    return [energies[i] for i in order]


def CalculateMMFFCharges(
    mol: rdChem.Mol,
    forcefield: Literal["MMFF94", "MMFF94s"] = "MMFF94",
    normalize_partial_charges: bool = True,
) -> np.ndarray:
    """Calculate MMFF charges for molecule"""
    forcefield = forcefield.upper()
    if forcefield == "MMFF94S":
        forcefield = "MMFF94s"
    mps = rdAllChem.MMFFGetMoleculeProperties(mol, forcefield)
    if mps is None:
        molstr = rdChem.MolToSmiles(mol)
        raise ValueError(f"MMFF charges could not be computed for {molstr}")
    n_atoms = mol.GetNumAtoms()
    charges = np.array([mps.GetMMFFPartialCharge(i) for i in range(n_atoms)])

    if normalize_partial_charges:
        total_charge = rdChem.GetFormalCharge(mol)
        partial_charges = charges.sum()
        offset = (total_charge - partial_charges) / n_atoms
        charges += offset
    return charges


def CalculateElectrostaticEnergy(
    mol: rdChem.Mol,
    forcefield: Literal["MMFF94", "MMFF94s"] = "MMFF94",
) -> np.ndarray:
    """Calculate electrostatic energy of all conformers using force field

    Returns
    -------
    energies: numpy.ndarray
        Array of energies, one for each conformer
    """
    from .utils import compute_atom_distance_matrix

    conformers = np.array([c.GetPositions() for c in mol.GetConformers()])
    distances = compute_atom_distance_matrix(conformers)
    inverse_distances = np.reciprocal(
        distances, out=np.zeros_like(distances), where=~np.isclose(distances, 0)
    )

    charges = np.abs(CalculateMMFFCharges(mol, forcefield)).reshape(-1, 1)
    charge_products = charges @ charges.T

    excl_i, excl_j = zip(*GetExclusions(mol))
    charge_products[(excl_i, excl_j)] = 0.0
    charge_products[(excl_j, excl_i)] = 0.0

    energies = inverse_distances * charge_products
    return 0.5 * energies.sum(axis=(1, 2))


def SortConformersByElectrostaticInteraction(
    mol: rdChem.Mol,
    forcefield: Literal["MMFF94", "MMFF94s"] = "MMFF94",
):
    """Sort conformers in-place by electrostatic energy using MMFF"""
    from .rdmolops import ReorderConformers

    energies = CalculateElectrostaticEnergy(mol, forcefield)
    order = np.argsort(energies)
    ReorderConformers(mol, order)


def RemoveConformersOutsideEnergyWindow(
    mol: rdChem.Mol,
    energyWindow: float = 30.0,
    forcefield: rdForceFieldHelpers.RDKIT_FF_TYPE = "MMFF94",
    numThreads: int = 1,
    ffVdwThresh: float = 10.0,
    ffNonBondedThresh: float = 100,
    ffIgnoreInterfragInteractions: bool = True,
) -> int:
    """Remove conformers outside energy window using force field, in-place

    The window covers an energy range from the conformer with the lowest
    energy. The molecule also has its conformers sorted by force field
    energy.

    Returns
    -------
    numConfs: int
        The number of remaining conformers
    """
    from .rdmolops import KeepConformerIds

    if energyWindow < 0:
        return mol.GetNumConformers()

    energies = SortConformersByEnergy(
        mol,
        forcefield=forcefield,
        numThreads=numThreads,
        ffVdwThresh=ffVdwThresh,
        ffNonBondedThresh=ffNonBondedThresh,
        ffIgnoreInterfragInteractions=ffIgnoreInterfragInteractions,
        reverse=False,
    )
    lowest = energies[0]
    highest = lowest + energyWindow
    conf_ids = [conf.GetId() for conf in mol.GetConformers()]
    mask = np.array(energies) <= highest
    keep = np.array(conf_ids)[mask]
    KeepConformerIds(mol, keep)

    return mol.GetNumConformers()
