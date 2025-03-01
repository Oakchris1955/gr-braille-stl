import itertools
import pathlib
import os
from typing import Dict, List, Optional

from braille_symbol import BrailleSymbol
import csv_loader

PARENT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
BASE_PATH = os.path.join(PARENT_PATH, "maps")

class NonExistentLocale(Exception):
    locale: str

    def __init__(self, locale):
        self.locale = locale
    def __str__(self):
        return f"Locale \"{self.locale}\" not found"

class Locale:
    entries: Dict[str, Dict[str, BrailleSymbol]]

    def __init__(self, cc: str):
        self.entries = _import_locale(cc)

    def is_char_valid(self, c: str) -> bool:
        return any(c in entry_values for entry_values in self.entries.values())

    def get_symbol(self, c: str) -> Optional[BrailleSymbol]:
        return next(entry_values[c] for entry_values in self.entries.values() if c in entry_values)

    def get_chars(self) -> List[str]:
        filtered_entries = {k: v for k, v in self.entries.items() if k != "special"}
        return [value for entry_values in filtered_entries.values() for value in entry_values]

def _import_locale(cc: str):
    """Import a Braille locale

    Keyword arguments:
    cc -- an ISO 3166-1 alpha-2 (two-letter) country code
    """

    entries = {}

    target_path = f"{BASE_PATH}/{cc}"

    if not os.path.isdir(target_path):
        raise NonExistentLocale(cc)

    for f in os.listdir(target_path):
        f = os.path.join(target_path, f)

        if not os.path.isfile(f):
            continue

        p = pathlib.Path(f)

        if p.suffix != ".csv":
            continue

        entries[p.stem.lower()] = csv_loader.load(f)

    return entries
