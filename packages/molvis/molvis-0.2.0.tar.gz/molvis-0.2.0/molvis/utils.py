import itertools


ATOM_COLOURS = {
    "H": "#999999",
    "Li": "#9932CC",
    "Na": "#9932CC",
    "K": "#9932CC",
    "Rb": "#9932CC",
    "Cs": "#9932CC",
    "Fr": "#9932CC",
    "Be": "#4E7566",
    "Mg": "#4E7566",
    "Ca": "#4E7566",
    "Sr": "#4E7566",
    "Ba": "#4E7566",
    "Ra": "#4E7566",
    "Sc": "#4E7566",
    "Y": "#4E7566",
    "La": "#4E7566",
    "Ac": "#4E7566",
    "Ti": "#301934",
    "V": "#301934",
    "Cr": "#301934",
    "Mn": "#301934",
    "Fe": "#301934",
    "Ni": "#301934",
    "Co": "#301934",
    "Cu": "#301934",
    "Zn": "#301934",
    "Zr": "#301943",
    "Nb": "#301943",
    "Mo": "#301943",
    "Tc": "#301943",
    "Ru": "#301943",
    "Rh": "#301943",
    "Pd": "#301943",
    "Ag": "#301943",
    "Cd": "#301943",
    "Hf": "#301934",
    "Ta": "#301934",
    "W": "#301934",
    "Re": "#301934",
    "Os": "#301934",
    "Ir": "#301934",
    "Pt": "#301934",
    "Au": "#301934",
    "Hg": "#301934",
    "B": "#FFFF00",
    "C": "#696969",
    "N": "#0000FF",
    "O": "#FF0000",
    "F": "#228B22",
    "Al": "#800080",
    "Si": "#FF7F50",
    "P": "#FF00FF",
    "S": "#FFFF00",
    "Cl": "#228B22",
    "As": "#F75394",
    "Br": "#4A2600",
    "other": "#3f3f3f"
}


def flatten(_list):
    """
    Flattens a list of lists by one subdimension

    e.g. [[1,2,3],[[2,3,4]]] ---> [1,2,3, [2,3,4]]

    Parameters
    ----------
    _list : list
        List of lists to be flattened

    Returns
    -------
    list
        Input list of lists flattened by one subdimension
    """

    _flist = list(itertools.chain(*_list))

    return _flist
