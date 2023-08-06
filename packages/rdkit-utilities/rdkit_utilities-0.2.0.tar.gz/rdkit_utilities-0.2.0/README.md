rdkit_utilities
==============================
[//]: # (Badges)
[![GitHub Actions Build Status](https://github.com/lilyminium/rdkit_utilities/workflows/CI/badge.svg)](https://github.com/lilyminium/rdkit_utilities/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/lilyminium/rdkit_utilities/branch/main/graph/badge.svg)](https://codecov.io/gh/lilyminium/rdkit_utilities/branch/main)
[![Documentation Status](https://readthedocs.org/projects/rdkit_utilities/badge/?version=latest)](https://rdkit_utilities.readthedocs.io/en/latest/?badge=latest)

Contained here are some helpful RDKit utilities for:

* generating conformers
    * ranking by MMFF electrostatic energy (for ELF conformer selection)
    * selecting to maximize diversity via RMS (for ELF conformer selection)
* finding symmetric atoms in a molecule
* finding the shell of neighbors around a central fragment, N bonds away


There are also convenience functions for:

* loading molecules from any input `MolFromInput`
* loading molecules from SMILES with keyword arguments for `removeHs`, etc.
* loading molecules and reordering by atom map number, analogous to the OpenFF toolkit `Molecule.from_mapped_smiles`
* generally reordering conformers
* optimizing molecules by specifying force field using a string name


Functions are in files such as `rdchem`, `rdDistGeom`, etc. to try to keep to
RDKit's organisation convention. Similarly to RDKit, a `Chem` and `AllChem`
are provided with group imports.
Functions are written in PascalCase and keyword arguments in camelCase, also to
keep to RDKit convention.
### Copyright

Copyright (c) 2022, Lily Wang


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.5.
