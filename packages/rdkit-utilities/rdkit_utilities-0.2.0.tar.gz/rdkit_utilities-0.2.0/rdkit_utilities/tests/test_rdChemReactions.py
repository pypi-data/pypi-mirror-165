from rdkit.Chem import rdChemReactions
from rdkit import Chem as rdChem
from rdkit_utilities import Chem
from rdkit_utilities.rdChemReactions import ClickReaction, CleanReaction


def test_run_click():
    rxn = rdChemReactions.ReactionFromSmarts(
        "[C:1](=[O:2])O.[N:3][H]>>[C:1](=[O:2])[N:3]"
    )
    cooh = "[H:5]-[C:1](=[O:2])-[O:3]-[H:4]"
    cnc = "[C:1](-[H:2])(-[H:3])(-[H:4])-[N:5](-[H:6])-[C:7](-[H:8])(-[H:9])(-[H:10])"
    reacts = (
        Chem.MolFromSmarts(
            cooh, orderByMapNumber=True, clearAtomMapNumbers=True, asQueryAtoms=False
        ),
        Chem.MolFromSmarts(
            cnc, orderByMapNumber=True, clearAtomMapNumbers=True, asQueryAtoms=False
        ),
    )
    products = ClickReaction(rxn, reacts)
    assert len(products) == 1

    product = products[0]
    expected = rdChem.AddHs(rdChem.MolFromSmiles("CN(C)C=O"))
    assert product.GetSubstructMatch(expected)
    assert expected.GetSubstructMatch(product)


def test_CleanReaction():
    rxn = rdChemReactions.ChemicalReaction()
    rct1 = rdChem.MolFromSmiles("[C:1](=[O:2])O")
    rct2 = Chem.MolFromSmiles("[N:3][H]", removeHs=False)
    prod = Chem.MolFromSmiles("[C:1](=[O:2])[N:3]")
    rxn.AddReactantTemplate(rct1)
    rxn.AddReactantTemplate(rct2)
    rxn.AddProductTemplate(prod)

    reactant1 = Chem.MolFromSmarts("[H:5]-[C:1](=[O:2])-[O:3]-[H:4]")
    reactant2 = Chem.MolFromSmarts(
        "[C:1](-[H:2])(-[H:3])(-[H:4])-[N:5](-[H:6])-[C:7](-[H:8])(-[H:9])(-[H:10])"
    )

    reaction, reactants = CleanReaction(rxn, (reactant1, reactant2))
    for reactant in reaction.GetReactants():
        for atom in reactant.GetAtoms():
            assert isinstance(atom, rdChem.QueryAtom)

    for reactant in reactants:
        for atom in reactant.GetAtoms():
            assert not isinstance(atom, rdChem.QueryAtom)

    products = reaction.RunReactants(reactants)
    assert len(products) == 1
    product = products[0][0]
    expected = rdChem.AddHs(rdChem.MolFromSmiles("CN(C)C=O"))
    assert product.GetSubstructMatch(expected)
    assert expected.GetSubstructMatch(product)
