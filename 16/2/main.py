Point = tuple[int, int]
Dir = str

dir_to_offset = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}


class Grid:
    def apply(self, dir: Dir):
        assert dir in dir_to_offset
        return [(dir, dir_to_offset[dir])]


# |
class VerticalSplitter(Grid):
    def apply(self, dir: Dir):
        if dir in "v^":
            return [(dir, dir_to_offset[dir])]

        return [[c, dir_to_offset[c]] for c in "v^"]


# -
class HorizontalSplitter(Grid):
    def apply(self, dir: Dir):
        if dir in "><":
            return [(dir, dir_to_offset[dir])]

        return [[c, dir_to_offset[c]] for c in "><"]


# /
class ForwardMirror(Grid):
    def apply(self, dir: Dir):
        mapping = {">": "^", "<": "v", "^": ">", "v": "<"}

        mapped = mapping[dir]
        return [(mapped, dir_to_offset[mapped])]


# \
class BackwardMirror(Grid):
    def apply(self, dir: Dir):
        mapping = {">": "v", "<": "^", "^": "<", "v": ">"}

        mapped = mapping[dir]
        return [(mapped, dir_to_offset[mapped])]


grid_types = {
    ".": Grid(),
    "|": VerticalSplitter(),
    "-": HorizontalSplitter(),
    "/": ForwardMirror(),
    "\\": BackwardMirror(),
}


def evaluate(grid: dict[Point, Grid], start: tuple[Point, Dir]):
    visited: set[tuple[Point, Dir]] = set()
    queue: list[tuple[Point, Dir]] = [start]

    while any(queue):
        point, dir = queue.pop(0)
        visited.add((point, dir))
        for new_dir, offset in grid[point].apply(dir):
            new_point = (point[0] + offset[0], point[1] + offset[1])
            if (new_point, new_dir) not in visited and new_point in grid:
                queue.append((new_point, new_dir))

    return len(set([point for point, _ in visited]))


def solve(input_lines: list[str]):
    grid: dict[Point, Grid] = {(x, y): grid_types[c] for y, line in enumerate(input_lines) for x, c in enumerate(line)}

    starts = [
        *[((0, i), ">") for i in range(len(input_lines))],
        *[((len(input_lines[0]) - 1, i), "<") for i in range(len(input_lines))],
        *[((i, 0), "v") for i in range(len(input_lines[0]))],
        *[((i, len(input_lines) - 1), "^") for i in range(len(input_lines[0]))],
    ]

    return max(evaluate(grid, start) for start in starts)


def main():
    with open("16/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
