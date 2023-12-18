import re

Point = tuple[int, int]
Direction = tuple[int, int]

DIRECTIONS: dict[str, Direction] = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


def draw_vertecies(
    vertecies: list[Point], edges: list[tuple[Point, Point]], areas: list[tuple[Point, Point]], scale: int = 100_000
):
    vertecies_scaled = [(x // scale, y // scale) for x, y in vertecies]
    xs = sorted(set(x for x, _ in vertecies_scaled))
    ys = sorted(set(y for _, y in vertecies_scaled))
    x_offset, x_range = xs[0], xs[-1] - xs[0]
    y_offset, y_range = ys[0], ys[-1] - ys[0]
    edges_scaled = [
        ((x1 // scale - x_offset, y1 // scale - y_offset), (x2 // scale - x_offset, y2 // scale - y_offset))
        for (x1, y1), (x2, y2) in edges
    ]
    areas_scaled = [
        ((x1 // scale - x_offset, y1 // scale - y_offset), (x2 // scale - x_offset, y2 // scale - y_offset))
        for (x1, y1), (x2, y2) in areas
    ]

    grid = [["." for _ in range(x_range + 1)] for _ in range(y_range + 1)]

    for i, (p1, p2) in enumerate(areas_scaled):
        for x in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1):
            for y in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1):
                grid[y][x] = "ABCDEFGHIJKLMNOPQRSUVWXYZ"[i % 25]

    for p1, p2 in edges_scaled:
        for x in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1):
            for y in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1):
                grid[y][x] = "#"

    for x, y in vertecies_scaled:
        grid[y - y_offset][x - x_offset] = "X"
    grid[-y_offset][-x_offset] = "@"

    for row in grid:
        print("".join(row))


def solve(input_lines: list[str]):
    parser_re = re.compile(r"^(?P<dir>[UDLR])\s(?P<count>\d+)\s\(#(?P<colour>[0-9a-f]{6})\)$")

    parsed = [
        ("RDLU"[int(m.group("colour")[5])], int(m.group("colour")[:5], 16))
        for line in input_lines
        if (m := parser_re.match(line))
    ]

    cursor = (0, 0)
    vertecies = []
    for d, c in parsed:
        direction = DIRECTIONS[d]
        cursor = (cursor[0] + direction[0] * c, cursor[1] + direction[1] * c)
        vertecies.append(cursor)
    assert cursor == (0, 0)

    xs = sorted(set(x for x, _ in vertecies))
    ys = sorted(set(y for _, y in vertecies))

    edges = []
    for p1, p2 in zip(vertecies[-1:] + vertecies[:-1], vertecies):
        px = sorted([p1[0], p2[0]])
        py = sorted([p1[1], p2[1]])
        inner_vertecies = []
        for i in range(xs.index(px[0]), xs.index(px[1]) + 1):
            for j in range(ys.index(py[0]), ys.index(py[1]) + 1):
                inner_vertecies.append((xs[i], ys[j]))
        edges.extend(zip(inner_vertecies, inner_vertecies[1:]))

    grid = {
        (i, j): {
            (0, -1): ((xs[i], ys[j]), (xs[i + 1], ys[j])),
            (0, 1): ((xs[i], ys[j + 1]), (xs[i + 1], ys[j + 1])),
            (-1, 0): ((xs[i], ys[j]), (xs[i], ys[j + 1])),
            (1, 0): ((xs[i + 1], ys[j]), (xs[i + 1], ys[j + 1])),
        }
        for i in range(len(xs) - 1)
        for j in range(len(ys) - 1)
    }

    grid_queue: list[Point] = [(xs.index(0), ys.index(0))]
    seen = set()

    while grid_queue:
        p = grid_queue.pop()

        for direction, edge in grid[p].items():
            if edge in edges:
                continue
            next_p = (p[0] + direction[0], p[1] + direction[1])

            if next_p in seen or next_p not in grid:
                continue
            seen.add(next_p)

            grid_queue.append(next_p)

    area = 0

    areas = []

    edges_added = set()
    vertecies_added = set()

    for s in seen:
        v = grid[s]
        p1 = v[(0, -1)][0]
        p2 = v[(0, 1)][1]
        inner_area = (p2[0] - p1[0] - 1) * (p2[1] - p1[1] - 1)
        area += inner_area
        for edge in v.values():
            if edge not in edges_added:
                edges_added.add(edge)
                area += (edge[1][1] - edge[0][1] - 1) if edge[0][0] == edge[1][0] else (edge[1][0] - edge[0][0] - 1)
            for p in edge:
                if p not in vertecies_added:
                    vertecies_added.add(p)
                    area += 1
        areas.append((p1, p2))

    print("=====")
    draw_vertecies(vertecies, edges, areas)

    return area


def main():
    with open("18/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
