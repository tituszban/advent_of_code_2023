from typing import Optional
from itertools import combinations


class Line:
    def __init__(self, line: str):
        p, v = line.split(" @ ")
        self.x, self.y, self.z = map(int, p.split(", "))
        self.vx, self.vy, self.vz = map(int, v.split(", "))

    @property
    def x1(self):
        return self.x

    @property
    def x2(self):
        return self.x + self.vx

    @property
    def y1(self):
        return self.y

    @property
    def y2(self):
        return self.y + self.vy

    def __repr__(self):
        return f"Line({self.x}, {self.y}, {self.z} @ {self.vx}, {self.vy}, {self.vz})"

    def get_t(self, x: float) -> float:
        return (x - self.x) / self.vx


# Ref: https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Formulas
def get_intersection(l1: Line, l2: Line) -> Optional[tuple[float, float]]:
    x1, x2 = l1.x1, l1.x2
    x3, x4 = l2.x1, l2.x2
    y1, y2 = l1.y1, l1.y2
    y3, y4 = l2.y1, l2.y2

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
        return None

    numerator_x = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    numerator_y = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)

    return (numerator_x / denominator, numerator_y / denominator)


def solve(input_lines: list[str], min_v: int = 200000000000000, max_v: int = 400000000000000):
    lines = list(map(Line, input_lines))

    count = 0
    for l1, l2 in combinations(lines, 2):
        intersection = get_intersection(l1, l2)
        if intersection is None:
            continue
        x, y = intersection
        if l1.get_t(x) < 0 or l2.get_t(x) < 0:
            continue
        if min_v <= x <= max_v and min_v <= y <= max_v:
            count += 1

    return count


def main():
    with open("24/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
