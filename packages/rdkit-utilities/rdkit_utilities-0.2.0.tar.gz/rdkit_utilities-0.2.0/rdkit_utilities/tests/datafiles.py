from pkg_resources import resource_filename


def datapath(path):
    return resource_filename(__name__, f"data/{path}")


CCH_PDB = datapath("cch.pdb")
