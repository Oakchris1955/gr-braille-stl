from typing import List
import build123d as bd

from braille_symbol import BrailleSymbol

class CADParams:
    dot_radius: float
    cell_width: float
    cell_height: float
    dot_height: float

    def __init__(self, dot_radius: float, cell_width: float, cell_height: float, dot_height: float):
        self.dot_radius = dot_radius
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.dot_height = dot_height

    @classmethod
    def from_radius_and_height(cls, radius: float, height: float):
        return cls(radius, radius * 4, height / 2, height / 2)

    def symbol_width(self) -> float:
        return self.cell_width * 2

    def symbol_length(self) -> float:
        return self.cell_width * 3

    def symbol_height(self) -> float:
        return self.dot_height + self.cell_height


#def _generate_dots(symbols: List[BrailleSymbol], params: CADParams) -> bd.Part:


def braille_to_stl(symbols: List[BrailleSymbol], params: CADParams, dest_file: str):
    total_width = len(symbols) * params.symbol_width()

    # the coordinates we give are the center of the box, but we want one edge to be at the axis origin
    base = bd.Pos(total_width / 2, params.symbol_length() / 2, params.cell_height / 2) * bd.Box(total_width, params.symbol_length(), params.cell_height)

    dot_cylinder = bd.extrude(bd.Circle(params.dot_radius), params.symbol_height())

    dots = bd.Part()

    symbol_pos = bd.Vector(+params.cell_width / 2, -params.cell_width / 2 + params.cell_width * 3, 0)

    for symbol in symbols:
        for i, dot in enumerate(symbol.dots):
            if dot:
                dots += bd.copy_module.copy(dot_cylinder).locate(bd.Pos(symbol_pos))

            symbol_pos.Y -= params.cell_width

            if (i+1) % 3 == 0:
                symbol_pos.Y += params.cell_width * 3
                symbol_pos.X += params.cell_width

    out = base + dots

    exporter = bd.Mesher()
    # this make this script a bit quicker and reduces the file size too
    exporter.add_shape(out, angular_deflection=1)
    exporter.write(dest_file)

