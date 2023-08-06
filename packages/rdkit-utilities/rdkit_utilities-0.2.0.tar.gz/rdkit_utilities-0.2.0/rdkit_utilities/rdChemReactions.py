from typing import Tuple, List
import itertools

from rdkit import Chem as rdChem
from rdkit.Chem import rdChemReactions


def ClickReaction(
    reaction: rdChemReactions.ChemicalReaction,
    reactants: Tuple[rdChem.Mol, ...],
) -> List[rdChem.Mol]:
    """Run a "click" reaction by manually building a molecule

    Occasionally an RDKit ChemicalReaction.RunReactants won't work.
    If a product is fully tagged and specified, you can try running
    this click reaction instead.

    Note that this does not do any fancy chemistry inferring.
    You will need to specify any hydrogens you want to remove, for example.
    """
    rdproducts = reaction.GetProducts()
    if len(rdproducts) != 1:
        raise ValueError(
            "This function is only supported for reactions with 1 product. "
            f"The reaction given has {len(rdproducts)} products"
        )

    rdproduct = rdproducts[0]
    product_map_numbers = [atom.GetAtomMapNum() for atom in rdproduct.GetAtoms()]
    if 0 in product_map_numbers:
        raise ValueError(
            "Reaction product must have every atom tagged with a map number. "
            f"Given: {rdChem.MolToSmarts(rdproduct)}"
        )

    rdreactants = list(reaction.GetReactants())
    if not len(rdreactants) == len(reactants):
        raise ValueError(
            "`reactants` must have same length as reactants in `reaction`. "
            f"Given {len(reactants)} reactants for {len(rdreactants)} in reaction"
        )

    ORIGINAL_MAP_NUMBER = "_original_map_num"

    edited_reactants = []
    for rdreactant, reactant in zip(rdreactants, reactants):
        rd_map_numbers = [atom.GetAtomMapNum() for atom in rdreactant.GetAtoms()]
        indices_to_keep = []
        indices_to_delete = []
        for i, x in enumerate(rd_map_numbers):
            if x not in product_map_numbers:
                indices_to_delete.append(i)
            else:
                indices_to_keep.append(i)

        reactant_list = []
        for match in reactant.GetSubstructMatches(rdreactant):
            # cut bonds to atoms we want to delete
            to_delete = sorted([match[i] for i in indices_to_delete])
            reactant_ = rdChem.RWMol(reactant)
            for atom in reactant_.GetAtoms():
                atom.SetIntProp(ORIGINAL_MAP_NUMBER, atom.GetAtomMapNum())
                atom.SetAtomMapNum(0)

            for i in indices_to_keep:
                atom = reactant_.GetAtomWithIdx(match[i])
                atom.SetAtomMapNum(rd_map_numbers[i])

            for i in to_delete[::-1]:
                atom_ = reactant_.GetAtomWithIdx(i)
                for bond in atom_.GetBonds():
                    reactant_.RemoveBond(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx())
            # keep only one fragment
            mapping = []
            fragments = rdChem.GetMolFrags(
                reactant_, asMols=True, sanitizeFrags=False, fragsMolAtomMapping=mapping
            )
            for i, fragment_indices in enumerate(mapping):
                if all(match[x] in fragment_indices for x in indices_to_keep):
                    reactant_list.append(fragments[i])
                    break
        edited_reactants.append(reactant_list)

    rwproducts: List[rdChem.Mol] = []
    for group in itertools.product(*edited_reactants):
        rwproduct = rdChem.Mol()
        for reactant in group:
            rwproduct = rdChem.CombineMols(rwproduct, reactant)
            rwproduct = rdChem.RWMol(rwproduct)

        index_to_map_numbers = {
            atom.GetIdx(): atom.GetAtomMapNum()
            for atom in rwproduct.GetAtoms()
            if atom.GetAtomMapNum()
        }

        map_to_index_numbers = {v: k for k, v in index_to_map_numbers.items()}

        # add required bonds
        for bond in rdproduct.GetBonds():
            i = map_to_index_numbers[bond.GetBeginAtom().GetAtomMapNum()]
            j = map_to_index_numbers[bond.GetEndAtom().GetAtomMapNum()]
            rwbond = rwproduct.GetBondBetweenAtoms(i, j)
            if rwbond is None:
                rwproduct.AddBond(i, j, bond.GetBondType())
            else:
                rwproduct.ReplaceBond(rwbond.GetIdx(), bond)

        for atom in rwproduct.GetAtoms():
            if atom.HasProp(ORIGINAL_MAP_NUMBER):
                atom.SetAtomMapNum(atom.GetIntProp(ORIGINAL_MAP_NUMBER))
                atom.ClearProp(ORIGINAL_MAP_NUMBER)

        rwproduct.UpdatePropertyCache()
        rwproducts.append(rwproduct)
    return rwproducts


def CleanReaction(
    reaction: rdChemReactions.ChemicalReaction,
    reactants: Tuple[rdChem.Mol, ...],
) -> Tuple[rdChemReactions.ChemicalReaction, Tuple[rdChem.Mol, ...]]:
    """Clean RDKit reaction and reactants by converting them to QueryAtoms or Atoms respectively"""
    from .rdmolops import MolAsMolWithAtoms, MolAsMolWithQueryAtoms

    new_reaction = rdChemReactions.ChemicalReaction()
    for reactant in reaction.GetReactants():
        new_reactant = MolAsMolWithQueryAtoms(reactant)
        new_reactant.UpdatePropertyCache()
        new_reaction.AddReactantTemplate(new_reactant)
    for product in reaction.GetProducts():
        new_product = MolAsMolWithQueryAtoms(product)
        new_product.UpdatePropertyCache()
        new_reaction.AddProductTemplate(new_product)

    reactants = tuple(MolAsMolWithAtoms(mol) for mol in reactants)
    for reactant in reactants:
        reactant.UpdatePropertyCache()
    return new_reaction, reactants


def RunOrClickReaction(
    reaction: rdChemReactions.ChemicalReaction,
    reactants: Tuple[rdChem.Mol, ...],
    clean: bool = True,
) -> Tuple[Tuple[rdChem.Mol, ...]]:
    """Try running reaction, or default to ClickReaction if it does not"""
    if clean:
        reaction, reactants = CleanReaction(reaction, reactants)
    products = reaction.RunReactants(reactants)
    if not products:
        products = ClickReaction(reaction, reactants)
        products = tuple((x,) for x in products)
    return products
