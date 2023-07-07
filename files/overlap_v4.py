import sys
from collections.abc import Iterable
from typing import Optional
from dataclasses import dataclass

@dataclass
class Rectangle:
    x1: float
    y1: float
    x2: float
    y2: float

    def __post_init__(self):
        self.x1, self.x2 = min(self.x1, self.x2), max(self.x1, self.x2)
        self.y1, self.y2 = min(self.y1, self.y2), max(self.y1, self.y2)

    @classmethod
    def from_list(cls, coordinates: list[float]):
        if len(coordinates) != 4:
            raise ValueError(f"Incorrect number of coordinates for '{coordinates}'")
        x1, y1, x2, y2 = coordinates
        return cls(x1=x1, y1=y1, x2=x2, y2=y2)

    def area(self):
        return (self.x2-self.x1) * (self.y2-self.y1)


def main(infile, outfile):
    rectangles = read_rectangles(infile)

    for red_name, red_coords in rectangles.items():
        output_line = []
        for blue_name, blue_coords in rectangles.items():
            result = '1' if rects_overlap(red_coords, blue_coords) else '0'

            output_line.append(result)
        outfile.write('\t'.join(output_line) + '\n')


def read_rectangles(rectangles: Iterable[str]) -> dict[str, list[float]]:
    result = {}
    for rectangle in rectangles:
        name, *coords = rectangle.split()
        try:
            value = [float(c) for c in coords]
        except ValueError:
            raise ValueError(f"Non numeric value provided as input for '{rectangle}'")

        if len(value) != 4:
            raise ValueError(f"Incorrect number of coordinates for '{rectangle}'")

        # make sure x1 <= x2, value = [x1, y1, x2, y2]
        value[0], value[2] = min(value[0], value[2]), max(value[0], value[2])
        value[1], value[3] = min(value[1], value[3]), max(value[1], value[3])
        result[name] = value
    return result


def rects_overlap(red, blue) -> Optional[list[float]]:
    red_lo_x, red_lo_y, red_hi_x, red_hi_y = red
    blue_lo_x, blue_lo_y, blue_hi_x, blue_hi_y = blue

    if (red_lo_x >= blue_hi_x) or (red_hi_x <= blue_lo_x) or \
            (red_lo_y >= blue_hi_y) or (red_hi_y <= blue_lo_y):
        return None

    x1 = max(red_lo_x, blue_lo_x)
    y1 = max(red_lo_y, blue_lo_y)
    x2 = min(red_hi_x, blue_hi_x)
    y2 = min(red_hi_y, blue_hi_y)
    return [x1, y1, x2, y2]


if __name__ == "__main__":
    with open(sys.argv[1], encoding='utf-8') as infile, \
            open(sys.argv[2], 'w', encoding='utf-8') as outfile:
        main(infile, outfile)
