from dataclasses import dataclass
import networkx as nx


V2 = tuple[int, int]

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
OPPOSITE: dict[V2, V2] = {(0, 1): (0, -1), (0, -1): (0, 1), (1, 0): (-1, 0), (-1, 0): (1, 0)}
KEY = tuple[V2, V2]
START_DIR: V2 = (0, 1)


@dataclass(frozen=True)
class Segment:
    start: V2
    end: V2
    count: int


def build_segments(grid: dict[V2, str], start: V2, goal: V2):
    segments: set[Segment] = set()
    seen: set[V2] = set()

    def _go_to_next_intersection(p: V2, direction: V2) -> tuple[list[V2], V2]:
        assert p in grid
        assert direction in DIRECTIONS

        neighbours: list[KEY] = [
            (p_n, d) for d in DIRECTIONS if d != OPPOSITE[direction] and (p_n := (p[0] + d[0], p[1] + d[1])) in grid
        ]

        if len(neighbours) == 1:
            rest, end_dir = _go_to_next_intersection(*neighbours[0])
            return [p, *rest], end_dir
        return [p], direction

    def _get_segments(p: V2, direction: V2) -> tuple[list[V2], list[KEY]]:
        assert p in grid
        assert direction in DIRECTIONS

        neighbours: list[KEY] = [
            (p_n, d) for d in DIRECTIONS if d != OPPOSITE[direction] and (p_n := (p[0] + d[0], p[1] + d[1])) in grid
        ]

        if (n_l := len(neighbours)) <= 0:
            return [p], []
        if n_l == 1:
            rest, children = _get_segments(*neighbours[0])
            return [p, *rest], children

        return [p], neighbours

    to_visit: list[KEY] = [(start, START_DIR)]
    while to_visit:
        p, direction = to_visit.pop(0)
        neighbours: list[KEY] = [
            (p_n, d) for d in DIRECTIONS if d != OPPOSITE[direction] and (p_n := (p[0] + d[0], p[1] + d[1])) in grid
        ]
        for neighbour in neighbours:
            path, end_dir = _go_to_next_intersection(*neighbour)
            segments.add(Segment(p, path[-1], len(path)))
            if path[-1] not in seen:
                seen.add(path[-1])
                to_visit.append((path[-1], end_dir))

    return segments


def solve(input_lines: list[str]):
    grid = {(x, y): c for y, line in enumerate(input_lines) for x, c in enumerate(line) if c != "#"}

    start = (1, 0)
    goal = (len(input_lines[0]) - 2, len(input_lines) - 1)

    segments = build_segments(grid, start, goal)

    DG = nx.Graph()
    for segment in segments:
        DG.add_edge(segment.start, segment.end, weight=segment.count)
    weights = {
        **{(seg.start, seg.end): seg.count for seg in segments},
        **{(seg.end, seg.start): seg.count for seg in segments},
    }

    longest = max(
        map(lambda path: sum(weights[edge] for edge in zip(path, path[1:])), nx.all_simple_paths(DG, start, goal))
    )

    return longest


def main():
    with open("23/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
