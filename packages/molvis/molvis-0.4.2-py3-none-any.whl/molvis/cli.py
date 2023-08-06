"""
This is the command line interface to molvis
"""

import argparse
import os

from . import core


def show_func(args):
    """
    Wrapper for cli call to show

    Parameters
    ----------
        args : argparser object
            command line arguments

    Returns
    -------
        None

    """

    head = os.path.splitext(args.xyz_file)[0]

    ms1 = core.Model.from_xyz(args.xyz_file)

    if args.atom_style == 'ball_stick':
        ms1.atom_rep = 'sphere'
        ms1.atom_radii = 0.4
        ms_temp = core.Model.from_xyz(args.xyz_file)
        ms_temp.atom_rep = 'stick'
        ms_temp.atom_radii = 0.2
        extra_style = ms_temp.gen_set_style()
        ms1.extra_styles = extra_style
    else:
        ms1.atom_rep = args.atom_style

    viewer_1 = core.Viewer(objects=[ms1])

    page = core.HtmlPage(scripts=[viewer_1.script], body=[viewer_1.div])

    page.save(output="{}.html".format(head))

    print("{} saved to {}.html".format(args.xyz_file, head))

    if args.open:
        os.system("open {}.html".format(head))

    return


def read_args(arg_list=None):
    """
    Parser for command line arguments. Uses subparsers for individual programs

    Parameters
    ----------
        args : argparser object
            command line arguments

    Returns
    -------
        None

    """

    description = """
    A package for displaying xyz files and chemical structures
    """

    epilog = """
    To display options for a specific program, use molvis PROGRAMNAME -h
    """

    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="prog")

    show = subparsers.add_parser(
        "show",
        description="Creates html file to visualise structure in xyz file"
    )
    show.set_defaults(func=show_func)

    show.add_argument(
        "xyz_file",
        type=str,
        help="File containing xyz coordinates in .xyz format"
    )
    
    show.add_argument(
        "--atom_style",
        type=str,
        help="Style of atoms",
        choices=("stick", "sphere", "ball_stick"),
        default='stick'
    )

    show.add_argument(
        "--open",
        action='store_true',
        help="Open resulting .html file in browser"
    )

    # read sub-parser
    parser.set_defaults(func=lambda args: parser.print_help())
    args = parser.parse_args(arg_list)
    args.func(args)


def main():
    read_args()
