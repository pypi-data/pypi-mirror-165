from typing import Union, List, Tuple
from typing_extensions import Literal

from rdkit import Chem as rdChem
from rdkit.Chem import rdForceFieldHelpers as rdFF
from rdkit.ForceField.rdForceField import ForceField as RDForceField

RDKIT_FF_NAMES = ["UFF", "MMFF", "MMFF94", "MMFF94S"]
RDKIT_FF_NAME_TYPE = Literal[(*RDKIT_FF_NAMES,)]
RDKIT_FF_TYPE = Union[RDForceField, RDKIT_FF_NAME_TYPE]


def GetMoleculeForceField(
    mol: rdChem.Mol,
    forcefield: RDKIT_FF_NAME_TYPE = "MMFF94",
    ignoreInterfragInteractions: bool = True,
    vdwThresh: float = 10.0,
    nonBondedThresh: float = 100.0,
    confId: int = -1,
) -> RDForceField:
    """Get molecule force field with string

    Parameters
    ----------
    mol: rdkit.Chem.Mol
        Molecule of interest
    forcefield: Literal["UFF", "MMFF", "MMFF94", "MMFF94S"]
        Force field name. If an MMFF force field is used,
        you can choose the MMFF94 or MMFF94s variant.
        "MMFF" defaults to MMFF94.
    ignoreInterfragInteractions: bool
        If True, nonbonded terms between fragments will not be added to the forcefield.
    vdwThresh: float
        Used to exclude long-range van der Waals interactions.
        Only used for the UFF force field.
    nonBondedThresh: float
        Used to exclude long-range non-bonded interactions.
        Only used for the MMFF force field.
    confId: int
        Which conformer to optimize

    Returns
    -------
    rdkit.Chem.rdForceFieldHelpers.ForceField
    """

    forcefield = forcefield.upper()
    if forcefield not in RDKIT_FF_NAMES:
        raise ValueError(
            f"{forcefield} is not a supported force field. "
            "Supporte force fields: " + ", ".join(RDKIT_FF_NAMES)
        )
    if forcefield == "UFF":
        if not rdFF.UFFHasAllMoleculeParams(mol):
            raise ValueError(
                "MMFF force field does not contain all parameters "
                f"for given molecule: {rdChem.MolToSmarts(mol)}"
            )
        return rdFF.UFFGetMoleculeForceField(
            mol,
            vdwThresh=vdwThresh,
            confId=confId,
            ignoreInterfragInteractions=ignoreInterfragInteractions,
        )

    # associate MMFF with variants
    if forcefield == "MMFF":
        forcefield = "MMFF94"
    elif forcefield == "MMFF94S":
        forcefield = "MMFF94s"

    if not rdFF.MMFFHasAllMoleculeParams(mol):
        raise ValueError(
            "MMFF force field does not contain all parameters "
            f"for given molecule: {rdChem.MolToSmarts(mol)}"
        )
    molprops = rdFF.MMFFGetMoleculeProperties(mol, mmffVariant=forcefield)
    return rdFF.MMFFGetMoleculeForceField(
        mol,
        molprops,
        nonBondedThresh=nonBondedThresh,
        confId=confId,
        ignoreInterfragInteractions=ignoreInterfragInteractions,
    )


def FFOptimizeMolecule(
    mol: rdChem.Mol,
    forcefield: RDKIT_FF_TYPE = "MMFF94",
    maxIters: int = 200,
    vdwThresh: float = 10.0,
    nonBondedThresh: float = 100.0,
    confId: int = -1,
    ignoreInterfragInteractions: bool = True,
) -> int:
    """Optimize molecule

    Parameters
    ----------
    mol: rdkit.Chem.Mol
        Molecule of interest
    forcefield: Literal["UFF", "MMFF", "MMFF94", "MMFF94S"] or RDKit force field
        Force field name or RDKit force field.
        If an MMFF force field is used,
        you can choose the MMFF94 or MMFF94s variant.
        "MMFF" defaults to MMFF94.
    maxIters: int
        the maximum number of iterations
    ignoreInterfragInteractions: bool
        If True, nonbonded terms between fragments will not be added to the forcefield.
    vdwThresh: float
        Used to exclude long-range van der Waals interactions.
        Only used for the UFF force field.
    nonBondedThresh: float
        Used to exclude long-range non-bonded interactions.
        Only used for the MMFF force field.
    confId: int
        Which conformer to optimize

    Returns
    -------
    success: int
        0 if the optimization converged, 1 if more iterations are required.
    """
    if isinstance(forcefield, str):
        forcefield = GetMoleculeForceField(
            mol,
            forcefield=forcefield,
            vdwThresh=vdwThresh,
            nonBondedThresh=nonBondedThresh,
            confId=confId,
            ignoreInterfragInteractions=ignoreInterfragInteractions,
        )

    return rdFF.OptimizeMolecule(forcefield, maxIters=maxIters)


def FFOptimizeMoleculeConfs(
    mol: rdChem.Mol,
    forcefield: RDKIT_FF_TYPE = "MMFF94",
    maxIters: int = 200,
    numThreads: int = 1,
    vdwThresh: float = 10.0,
    nonBondedThresh: float = 100.0,
    confId: int = -1,
    ignoreInterfragInteractions: bool = True,
) -> List[Tuple[int, float]]:
    """Optimize molecule conformers

    Parameters
    ----------
    mol: rdkit.Chem.Mol
        Molecule of interest
    forcefield: Literal["UFF", "MMFF", "MMFF94", "MMFF94S"] or RDKit force field
        Force field name or RDKit force field.
        If an MMFF force field is used,
        you can choose the MMFF94 or MMFF94s variant.
        "MMFF" defaults to MMFF94.
    maxIters: int
        the maximum number of iterations
    numThreads: int
        the number of threads to use, only has an effect if the RDKit
        was built with thread support (defaults to 1).
        If set to zero, the max supported by the system will be used.
    ignoreInterfragInteractions: bool
        If True, nonbonded terms between fragments will not be added to the forcefield.
    vdwThresh: float
        Used to exclude long-range van der Waals interactions.
        Only used for the UFF force field.
    nonBondedThresh: float
        Used to exclude long-range non-bonded interactions.
        Only used for the MMFF force field.
    confId: int
        Which conformer to optimize

    Returns
    -------
    success_energies: List[Tuple[int, float]]
        List of tuples of (success, energy) for each conformer.
        The success is 0 if the optimization converged,
        1 if more iterations are required.
    """
    if isinstance(forcefield, str):
        forcefield = GetMoleculeForceField(
            mol,
            forcefield=forcefield,
            vdwThresh=vdwThresh,
            nonBondedThresh=nonBondedThresh,
            confId=confId,
            ignoreInterfragInteractions=ignoreInterfragInteractions,
        )

    return rdFF.OptimizeMoleculeConfs(
        mol,
        forcefield,
        maxIters=maxIters,
        numThreads=numThreads,
    )
