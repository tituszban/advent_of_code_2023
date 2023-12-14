from dataclasses import dataclass


@dataclass(frozen=True)
class Section:
    coordinates: tuple[tuple[int, int], ...]

    def fill(self, n: int):
        return self.coordinates[:n]

    @classmethod
    def from_list(cls, coordinates: list[tuple[int, int]]):
        return cls(tuple(coordinates))


class Sections:
    def __init__(self, sections: list[Section]):
        self._sections = sections
        self._mapping = {coordinate: section for section in sections for coordinate in section.coordinates}

    def apply_stones(self, stones: list[tuple[int, int]]):
        count_by_section = {section: 0 for section in self._sections}
        for stone in stones:
            count_by_section[self._mapping[stone]] += 1

        return [stone for section, count in count_by_section.items() for stone in section.fill(count)]


@dataclass
class GridSquare:
    c: str
    coordinate: tuple[int, int]


def rotate(grid: list[list[GridSquare]], n: int = 1):
    if n <= 0:
        return grid
    rotated = list(zip(*grid[::-1]))
    if n == 1:
        return rotated
    return rotate(rotated, n - 1)


def generate_sections(grid: list[list[GridSquare]]):
    columns: list[list[GridSquare]] = list(zip(*grid))
    sections: list[Section] = []
    for column in columns:
        coords: list[tuple[int, int]] = []
        for square in column:
            if square.c == "#":
                if len(coords) > 0:
                    sections.append(Section.from_list(coords))
                    coords = []
            else:
                coords.append(square.coordinate)
        if len(coords) > 0:
            sections.append(Section.from_list(coords))
    return Sections(sections)


def print_grid(grid: list[list[GridSquare]], stones: list[tuple[int, int]] = []):
    for line in grid:
        print("".join(["O" if square.coordinate in stones else square.c for square in line]))


def apply_gravity(sections: list[Sections], stones: list[tuple[int, int]], n: int):
    cache: dict[frozenset[tuple[int, int]], int] = {}
    reverse_cache: dict[int, list[tuple[int, int]]] = {}
    for i in range(n):
        for j in range(4):
            stones = sections[j].apply_stones(stones)

        stone_set = frozenset(stones)
        if stone_set in cache:
            loop_start = cache[stone_set]
            loop_length = i - loop_start
            o = (n - loop_start) % loop_length
            return reverse_cache[loop_start + o - 1]

        cache[stone_set] = i
        reverse_cache[i] = stones
    return stones


def evaluate_stones(stones: list[tuple[int, int]], height: int):
    return sum(height - stone[1] for stone in stones)


def solve(input_lines: list[str], n: int = 1000000000):
    grid = [
        [GridSquare("." if c in ".O" else "#", (x, y)) for x, c in enumerate(line)]
        for y, line in enumerate(input_lines)
    ]
    stones = [(x, y) for y, line in enumerate(input_lines) for x, c in enumerate(line) if c == "O"]

    rotated_sections = [generate_sections(rotate(grid, i)) for i in range(4)]

    print_grid(grid, stones)

    stones = apply_gravity(rotated_sections, stones, n)

    print("===")
    print_grid(grid, stones)

    return evaluate_stones(stones, len(grid))


def main():
    with open("14/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
