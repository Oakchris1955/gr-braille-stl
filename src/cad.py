import madcad
from typing import List

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


def braille_to_stl(symbols: List[BrailleSymbol], params: CADParams, dest_file: str):
    total_width = len(symbols) * params.symbol_width()

    base = madcad.generation.brick(
        madcad.vec3(0, 0, 0),
        madcad.vec3(total_width, params.symbol_length(), params.cell_height)
    )


    axis = madcad.Axis(madcad.O, madcad.Z)
    dot_circle = madcad.Circle(axis, params.dot_radius)
    mesh_circle = madcad.flatsurface(dot_circle)
    mesh_circle = madcad.extrusion(mesh_circle, madcad.Z * params.symbol_height())
    mesh_circle = mesh_circle.transform(madcad.translate(madcad.vec3(params.cell_width / 2, params.cell_width / 2, 0))).flip()

    # an empty mesh
    dots = madcad.Mesh()

    symbol_pos = madcad.vec3(0, 0, 0)

    for symbol in symbols:
        for i, dot in enumerate(symbol.dots):
            if dot:
                current_dot = mesh_circle.transform(madcad.translate(symbol_pos))
                dots = dots + current_dot

            symbol_pos += madcad.Y * params.cell_width

            if (i+1) % 3 == 0:
                symbol_pos -= madcad.Y * params.cell_width * 3
                symbol_pos += madcad.X * params.cell_width

    out = base + dots
    out = out.transform(madcad.scale(madcad.vec3(1, -1, 1))).flip()
    out.mergeclose()

    madcad.io.write(out, dest_file)

