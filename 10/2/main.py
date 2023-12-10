from dataclasses import dataclass


@dataclass(frozen=True, order=True, unsafe_hash=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    @property
    def left(self):
        return Point(self.y, -self.x)

    @property
    def right(self):
        return Point(-self.y, self.x)


NORTH = Point(0, -1)
SOUTH = Point(0, 1)
WEST = Point(-1, 0)
EAST = Point(1, 0)


@dataclass
class Node:
    kind: str
    location: Point

    @property
    def neighbours(self):
        return [
            point + self.location
            for point in {
                "|": [NORTH, SOUTH],
                "-": [WEST, EAST],
                "L": [NORTH, EAST],
                "J": [NORTH, WEST],
                "7": [SOUTH, WEST],
                "F": [SOUTH, EAST],
                ".": [],
                "S": [NORTH, SOUTH, WEST, EAST],
            }[self.kind]
        ]


def solve(input_lines: list[str]):
    start = None
    nodes: dict[Point, Node] = {}

    for y, line in enumerate(input_lines):
        for x, kind in enumerate(line):
            point = Point(x, y)
            node = Node(kind, point)
            if kind == "S":
                start = node
            nodes[point] = node

    assert start is not None

    def _get_loop() -> list[Point]:
        queue: list[tuple[Node, list[Point]]] = [(start, [])]

        while any(queue):
            node, history = queue.pop(0)
            neighbours = [nodes[n] for n in node.neighbours if n in nodes]
            valid_neighbours = [
                n for n in neighbours if node.location in n.neighbours and (not history or n.location != history[-1])
            ]

            for neighbour in valid_neighbours:
                if neighbour.location == start.location:
                    return [*history, node.location]
                queue.append((neighbour, [*history, node.location]))
        return []

    loop = [*_get_loop(), start.location]

    grid = {Point(x, y): "." for y, line in enumerate(input_lines) for x, _ in enumerate(line)}

    def _draw_grid():
        for y, line in enumerate(input_lines):
            print("".join(grid[Point(x, y)] for x, _ in enumerate(line)))

    inside_border = set()

    for next, point in zip(loop[1:], loop):
        grid[point] = "#"
        d = next - point
        if point in inside_border:
            inside_border.remove(point)

        def _mark_sides(_point):
            left = _point + d.left
            if grid.get(left) == ".":
                grid[left] = "L"
                if left in inside_border:
                    inside_border.remove(left)
            right = _point + d.right
            if grid.get(right) == ".":
                grid[right] = "R"
                inside_border.add(right)

        _mark_sides(point)
        _mark_sides(next)

    inside_queue = list(inside_border)
    count = 0
    while any(inside_queue):
        p = inside_queue.pop(0)
        count += 1

        for d in [NORTH, SOUTH, EAST, WEST]:
            p = p + d
            if grid.get(p) == ".":
                grid[p] = "R"
                inside_queue.append(p)

    _draw_grid()

    return count


def main():
    with open("10/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
