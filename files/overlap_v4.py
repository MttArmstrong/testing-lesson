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

    def overlap(self, other):
        if (self.x1 >= other.x2) or \
                (self.x2 <= other.x1) or \
                (self.y1 >= other.y2) or \
                (self.y2 <= other.y1):
            return None

        return Rectangle(
            x1=max(self.x1, other.x1),
            y1=max(self.y1, other.y1),
            x2=min(self.x2, other.x2),
            y2=min(self.y2, other.y2),
        )

    def rotate(self):
        return Rectangle(
            x1=self.y1,
            y1=-self.x1,
            x2=self.y2,
            y2=-self.x2,
        )


def main(infile, outfile):
    rectangles = read_rectangles(infile)

    for red_name, red_rect in rectangles.items():
        output_line = []
        for blue_name, blue_rect in rectangles.items():
            overlap = red_rect.overlap(blue_rect)
            result = str(overlap.area()) if overlap else '0'

            output_line.append(result)
        outfile.write('\t'.join(output_line) + '\n')


def read_rectangles(rectangles: Iterable[str]) -> dict[str, Rectangle]:
    result = {}
    for rectangle in rectangles:
        name, *coords = rectangle.split()
        try:
            value = [float(c) for c in coords]
        except ValueError:
            raise ValueError(f"Non numeric value provided as input for '{rectangle}'")

        result[name] = Rectangle.from_list(value)

    return result


if __name__ == "__main__":
    with open(sys.argv[1], encoding='utf-8') as infile, \
            open(sys.argv[2], 'w', encoding='utf-8') as outfile:
        main(infile, outfile)
