from typing import List
import build123d as bd

from braille_symbol import BrailleSymbol
import braille_constants as CONSTS

def _generate_dots(symbols: List[BrailleSymbol]) -> bd.Part:
    dot_cylinder = bd.Cylinder(CONSTS.DOT_DIAMETER / 2, CONSTS.DOT_HEIGHT * 2, align=bd.Align.MIN)

    dots = bd.Part()

    symbol_pos = bd.Vector(CONSTS.DOT_DISTANCE / 2, -CONSTS.DOT_DISTANCE / 2 + CONSTS.DOT_DISTANCE * 3, 0)

    for symbol in symbols:
        for i, dot in enumerate(symbol.dots):
            if dot:
                dots += bd.copy_module.copy(dot_cylinder).locate(bd.Pos(symbol_pos))

            symbol_pos.Y -= CONSTS.DOT_DISTANCE

            if (i+1) % 3 == 0:
                symbol_pos.Y += CONSTS.DOT_DISTANCE * 3
                symbol_pos.X += CONSTS.DOT_DISTANCE

        symbol_pos.X -= CONSTS.DOT_DISTANCE * 2
        symbol_pos.X += CONSTS.CELL_HORIZONTAL_DISTANCE

    return dots

def _generate_base(width: int, rows: int) -> bd.Part:
    # the coordinates we give are the center of the box, but we want one edge to be at the axis origin
    return bd.Box(width * CONSTS.CELL_HORIZONTAL_DISTANCE, rows * CONSTS.CELL_VERTICAL_DISTANCE, CONSTS.DOT_HEIGHT, align=bd.Align.MIN)

def braille_to_stl(symbols: List[List[BrailleSymbol]], dest_file: str):
    print("Generating mesh...")

    rows = len(symbols)
    width = max(len(s) for s in symbols)

    base = _generate_base(width, rows)
    dots = bd.Part()

    for i, s in enumerate(symbols):
        current_row = _generate_dots(s)
        current_row.position += (0, (rows - i - 1) * CONSTS.CELL_VERTICAL_DISTANCE, 0)
        dots += current_row

    print("Finalizing mesh (this may take a while)...")

    out = base + dots

    exporter = bd.Mesher()
    # this make this script a bit quicker and reduces the file size too
    exporter.add_shape(out, angular_deflection=10)
    exporter.write(dest_file)

