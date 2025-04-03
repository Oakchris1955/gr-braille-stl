#!/usr/bin/python3

import argparse

from braille_converter import text_to_braille
from cad import braille_to_stl

DEFAULT_RADIUS: float = 0.1
DEFAULT_HEIGHT: float = 0.2

def main():
    parser = argparse.ArgumentParser(
        prog="GRBrailleSTL",
        description="Ένα απλό πρόγραμμα μετατροπής κειμένου σε κώδικα Μπράιγ σε STL"
    )
    parser.add_argument('text', help="Το κείμενο που θέλετε να μεταφραστεί")
    parser.add_argument('dest', help="Η τοποθεσία του αρχείου εξόδου")
    parser.add_argument('-w', '--wrap-at', help="Αλλαγή γραμμής στα τόσα σύμβολα", type=int)

    args = parser.parse_args()

    s = [text_to_braille(t) for t in args.text.split(("\n"))]
    braille_to_stl(s, args.dest, args.wrap_at)

if __name__ == "__main__":
    main()