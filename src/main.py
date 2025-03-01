#!/usr/bin/python3

import argparse

from braille_converter import text_to_braille
from cad import braille_to_stl, CADParams

DEFAULT_RADIUS: float = 0.1
DEFAULT_HEIGHT: float = 0.2

def main():
    parser = argparse.ArgumentParser(
        prog="GRBrailleSTL",
        description="Ένα απλό πρόγραμμα μετατροπής κειμένου σε κώδικα Μπράιγ σε STL"
    )
    parser.add_argument('text', help="Το κείμενο που θέλετε να μεταφραστεί")
    parser.add_argument('dest', help="Η τοποθεσία του αρχείου εξόδου")
    parser.add_argument('-r', '--radius', help="Η ακτίνα των κουκίδων", type=float, default=DEFAULT_RADIUS)
    parser.add_argument('--height', help="Το συνολικό ύψος του STL μοντέλου", type=float, default=DEFAULT_HEIGHT)

    args = parser.parse_args()

    s = text_to_braille(args.text)
    braille_to_stl(s, CADParams.from_radius_and_height(args.radius, args.height), args.dest)

if __name__ == "__main__":
    main()