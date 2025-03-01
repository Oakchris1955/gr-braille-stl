from typing import Annotated, List

BRAILLE_BASEPOINT = 0x2800

class BrailleSymbol:
    dots: Annotated[list[bool], 6]

    def __init__(self, num: int):
        self.dots = []
        for _ in range(6):
            self.dots.insert(0, bool(num % 2))
            num //= 2

    def as_char(self) -> str:
        offset = 0
        for i, dot in enumerate(self.dots):
            if dot:
                offset += 2**i

        return chr(BRAILLE_BASEPOINT + offset)
