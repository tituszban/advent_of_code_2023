from dataclasses import dataclass


@dataclass(frozen=True, order=True, unsafe_hash=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


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
    grid: dict[Point, Node] = {}

    for y, line in enumerate(input_lines):
        for x, kind in enumerate(line):
            point = Point(x, y)
            node = Node(kind, point)
            if kind == "S":
                start = node
            grid[point] = node

    assert start is not None

    queue: list[tuple[Node, list[Point]]] = [(start, [])]
    visited = set()

    while any(queue):
        node, history = queue.pop(0)
        neighbours = [grid[n] for n in node.neighbours if n in grid]
        valid_neighbours = [
            n for n in neighbours if node.location in n.neighbours and (not history or n.location != history[-1])
        ]
        visited.add(node.location)

        for neighbour in valid_neighbours:
            if neighbour.location in visited:
                return len(history)
            queue.append((neighbour, [*history, node.location]))


def main():
    with open("10/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
