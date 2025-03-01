import csv
from typing import Dict

from braille_symbol import BrailleSymbol

def load(filename: str) -> Dict[str, BrailleSymbol]:
    out = {}

    with open(filename, "r") as f:
        reader = csv.reader(f)

        for row in reader:
            out[row[0]] = BrailleSymbol(int(row[1], base=2))

    return out
