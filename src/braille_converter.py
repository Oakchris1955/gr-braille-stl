from typing import List
import unicodedata

from braille_symbol import BrailleSymbol
import locales

class UnsupportedCharacter(Exception):
    def __str__(self):
        return "Unsupported character found"

def text_to_braille(text: str) -> List[BrailleSymbol]:
    out = []

    gr = locales.Locale("gr")
    xx = locales.Locale("xx")

    chars = gr.get_chars() + xx.get_chars()

    normalized_text = unicodedata.normalize("NFD", text)

    for c in normalized_text.lower():
        if c not in chars:
            print(f"UnsupportedCharacter \"{c}\"")
            raise UnsupportedCharacter

    def move_elements_back(lst, element):
        """Move all occurrences of the specified element back by one position in the list."""
        indices = [i for i, x in enumerate(lst) if x == element]  # Find all indices of the element

        for index in indices:
            # Move the element back if it is not at the first position
            if index > 0:
                # Swap with the previous element
                lst[index], lst[index - 1] = lst[index - 1], lst[index]

        return lst

    i = 0
    while i < len(normalized_text):
        c = normalized_text[i]

        if c.isupper():
            out.append(xx.entries["special"]["CAPITAL"])

        if c.isnumeric():
            out.append(xx.entries["special"]["NUMBER"])
            out.append(xx.entries["numerical"][c])
            i += 1
            continue

        # special handling for double vowels
        if c.lower() in set(map(lambda x: x[0], gr.entries["double_vowels"].keys())) and (i+1) != len(normalized_text):
            next_c = normalized_text[i+1].lower()
            double_letter = f"{c.lower()}{next_c}"
            if double_letter in gr.entries["double_vowels"]:
                out.append(gr.entries["double_vowels"][double_letter])
                i += 2
                continue

        out.append(gr.get_symbol(c.lower()))

        i += 1

    # before we return, we need to move every stress back by 1
    stress = gr.entries["misc"]["́"]

    out = move_elements_back(out, stress)

    return out


