from typing import List, Optional
import madcad
from math import pi

from braille_symbol import BrailleSymbol
import braille_constants as CONSTS

def _generate_dots(symbols: List[BrailleSymbol]) -> madcad.Mesh:
    dot_sphere = madcad.generation.uvsphere(
        madcad.vec3(0, 0, 0),
        radius=CONSTS.DOT_RADIUS,
    )

    dots = madcad.Mesh()

    symbol_pos = madcad.vec3(CONSTS.DOT_DISTANCE / 2, CONSTS.DOT_DISTANCE * 3, CONSTS.DOT_RADIUS)

    for symbol in symbols:
        for i, dot in enumerate(symbol.dots):
            if dot:
                dots += dot_sphere.transform(
                    madcad.translate(symbol_pos)
                )
            symbol_pos.y -= CONSTS.DOT_DISTANCE

            if (i+1) % 3 == 0:
                symbol_pos.y += CONSTS.DOT_DISTANCE * 3
                symbol_pos.x += CONSTS.DOT_DISTANCE

        symbol_pos.x -= CONSTS.DOT_DISTANCE * 2
        symbol_pos.x += CONSTS.CELL_HORIZONTAL_DISTANCE

    return dots

def _generate_base(width: int, rows: int) -> madcad.Mesh:
    # the coordinates we give are the center of the box, but we want one edge to be at the axis origin
    return madcad.generation.brick(
        madcad.vec3(0, 0, 0),
        madcad.vec3(width * CONSTS.CELL_HORIZONTAL_DISTANCE, rows * CONSTS.CELL_VERTICAL_DISTANCE, CONSTS.DOT_RADIUS)
    )

def braille_to_stl(symbols: List[List[BrailleSymbol]], dest_file: str, wrap_at: Optional[int]):
    # https://stackoverflow.com/a/1915307/
    # I could also use itertools' batched function, but it was
    # added pretty recently (in Python 3.12, less than two years ago)
    from itertools import islice

    def split_every(n, iterable):
        i = iter(iterable)
        piece = list(islice(i, n))
        while piece:
            yield piece
            piece = list(islice(i, n))
    if wrap_at is not None:
        new_symbols = []
        for row in symbols:
            new_symbols.extend(split_every(wrap_at, row))

        symbols = new_symbols

    print("Generating mesh...")

    rows = len(symbols)
    width = max(len(s) for s in symbols)

    base = _generate_base(width, rows)
    dots = madcad.Mesh()

    for i, s in enumerate(symbols):
        current_row = _generate_dots(s)
        current_row = current_row.transform(madcad.vec3(0, (rows - i - 1) * CONSTS.CELL_VERTICAL_DISTANCE, 0))
        dots += current_row

    print("Finalizing mesh (this may take a while)...")

    out = base + dots
    madcad.io.write(out, dest_file)
