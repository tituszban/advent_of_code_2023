from queue import PriorityQueue


V2 = tuple[int, int]

DIRECTIONS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]
OPPOSITE = {
    (0, 1): (0, -1),
    (0, -1): (0, 1),
    (1, 0): (-1, 0),
    (-1, 0): (1, 0)
}
ONE_WAY = {
    ">": (1, 0),
    "<": (-1, 0),
    "v": (0, 1),
    "^": (0, -1)
}
KEY = tuple[V2, V2]
START_DIR: V2 = (0, 1)


def build_segments(grid: dict[V2, str], start: V2, goal: V2):
    segments: dict[KEY, tuple[list[V2], list[KEY]]] = {}

    def _get_segments(p: V2, direction: V2) -> tuple[list[V2], list[KEY]]:
        assert p in grid
        assert direction in DIRECTIONS

        neighbours: KEY = [
            (p_n, d)
            for d in DIRECTIONS
            if d != OPPOSITE[direction] and (p_n := (p[0] + d[0], p[1] + d[1])) in grid and (grid[p] not in ONE_WAY or ONE_WAY[grid[p]] == d)]

        if (n_l := len(neighbours)) <= 0:
            return [p], []
        if n_l == 1:
            rest, children = _get_segments(*neighbours[0])
            return [p, *rest], children

        return [p], neighbours

    to_visit = [(start, START_DIR)]
    while to_visit:
        s, d = to_visit.pop(0)
        segment, children = _get_segments(s, d)
        if children or goal in segment:
            segments[(s, d)] = (segment, children)
        to_visit.extend(children)

    return segments


def explore(segments: dict[KEY, tuple[list[V2], list[KEY]]], start: V2, goal: V2):
    start_key = (start, START_DIR)

    end_points_cache = {}

    frontier = PriorityQueue()
    frontier.put((0, start_key, []))

    while not frontier.empty():
        cost, key, history = frontier.get()
        seg, children = segments[key]
        length = len(seg)
        final_junction = seg[-1]

        if any(p in history for p in seg):
            continue

        if end_points_cache.get(final_junction, [0])[0] >= cost + length:
            continue
        end_points_cache[final_junction] = (cost + length, [*history, *seg])

        for child in children:
            if child not in segments:
                continue
            frontier.put((cost + length, child, [*history, *seg]))

    return end_points_cache[goal]


def draw(input_lines: list[str], history: list[V2]):
    print("==")
    for y, line in enumerate(input_lines):
        print(''.join("O" if (x, y) in history else c for x, c in enumerate(line)))


def solve(input_lines: list[str]):
    grid = {(x, y): c for y, line in enumerate(input_lines)
            for x, c in enumerate(line) if c != "#"}

    start = (1, 0)
    goal = (len(input_lines[0]) - 2, len(input_lines) - 1)

    segments = build_segments(grid, start, goal)

    result, history = explore(segments, start, goal)

    # draw(input_lines, history)

    return result - 1


def main():
    with open("23/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
