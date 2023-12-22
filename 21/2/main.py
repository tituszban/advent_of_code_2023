# If you are reading this, I ask you not to judge for what I have committed here...
from itertools import product
import math
from queue import PriorityQueue
import json

V2 = tuple[int, int]

DIRECTIONS = (
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
)


def draw(input_lines: list[str], seen: set[V2]):
    print("====")
    for y, line in enumerate(input_lines):
        print("".join("O" if (x, y) in seen else c for x, c in enumerate(line) if (x + y) % 2 >= 0))


def walk_with_boundaries(grid: set[V2], start: list[V2], size: V2, boundaries: dict[str, set[V2]], n: int = 66):
    explore: PriorityQueue[tuple[int, V2]] = PriorityQueue()
    leaving_points: dict[str, tuple[int, set[V2]]] = {}
    all_boundaries = boundaries["LEFT"] | boundaries["RIGHT"] | boundaries["TOP"] | boundaries["BOTTOM"]
    for p in start:
        explore.put((0, p))

    seen = set()

    def _normalize(p: V2):
        return p[0] % size[0], p[1] % size[1]

    while not explore.empty():
        depth, point = explore.get()
        if point in seen:
            continue
        seen.add(point)

        if point in all_boundaries:
            for key, boundary in boundaries.items():
                if point in boundary:
                    if key not in leaving_points:
                        leaving_points[key] = (depth, set())
                    if depth <= leaving_points[key][0]:
                        leaving_points[key][1].add(_normalize(point))
            continue

        for step1, step2 in product(DIRECTIONS, repeat=2):
            mid_point = (point[0] + step1[0], point[1] + step1[1])
            if mid_point not in grid and mid_point not in all_boundaries:
                continue
            new_point = (mid_point[0] + step2[0], mid_point[1] + step2[1])

            if new_point not in grid and new_point not in all_boundaries:
                continue
            if new_point in seen:
                continue
            if depth + 2 > n:
                continue
            explore.put((depth + 2, new_point))

    return seen, leaving_points


def walk_limited(grid: set[V2], start: list[V2], n: int):
    explore: PriorityQueue[tuple[int, V2]] = PriorityQueue()

    for p in start:
        explore.put((0, p))

    seen = set()

    while not explore.empty():
        depth, point = explore.get()
        if point in seen:
            continue
        if point not in grid:
            continue
        seen.add(point)

        for step1, step2 in product(DIRECTIONS, repeat=2):
            mid_point = (point[0] + step1[0], point[1] + step1[1])
            if mid_point not in grid:
                continue
            new_point = (mid_point[0] + step2[0], mid_point[1] + step2[1])

            if new_point not in grid:
                continue
            if new_point in seen:
                continue
            if depth + 2 > n:
                continue
            explore.put((depth + 2, new_point))

    return seen


def walk_unlimited(grid: set[V2], start: list[V2], size: V2, n: int = 66):
    explore: PriorityQueue[tuple[int, V2]] = PriorityQueue()

    for p in start:
        explore.put((0, p))

    seen = set()

    def _normalize(p: V2):
        return p[0] % size[0], p[1] % size[1]

    while not explore.empty():
        depth, point = explore.get()
        if point in seen:
            continue
        seen.add(point)

        for step1, step2 in product(DIRECTIONS, repeat=2):
            mid_point = (point[0] + step1[0], point[1] + step1[1])
            if _normalize(mid_point) not in grid:
                continue
            new_point = (mid_point[0] + step2[0], mid_point[1] + step2[1])

            if _normalize(new_point) not in grid:
                continue
            if new_point in seen:
                continue
            if depth + 2 > n:
                continue
            explore.put((depth + 2, new_point))

    return seen


def load_boundaries() -> dict[V2, dict[str, tuple[int, list[V2]]]]:
    with open("21/.cache/cache.json") as f:
        data = json.load(f)
    return {
        tuple(map(int, k.split(","))): {kk: (vv[0], list(map(tuple, vv[1]))) for kk, vv in v.items()}
        for k, v in data.items()
    }  # type: ignore


NO_RETURN = {
    "TOP": "BOTTOM",
    "BOTTOM": "TOP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT",
}
DIRECTION_NAMES = ["BOTTOM", "LEFT", "RIGHT", "TOP"]
NAMES_TO_DIRECTIONS = {"BOTTOM": (0, 1), "TOP": (0, -1), "LEFT": (-1, 0), "RIGHT": (1, 0), "": (0, 0)}


def find_boundary_entries(grid: set[V2], size: V2, boundaries: dict[str, set[V2]], start: list[V2], n=150):
    explore: list[V2] = list(start)

    results: dict[V2, dict[str, tuple[int, set[V2]]]] = {}

    while explore:
        entry = explore.pop(0)
        if entry in results:
            continue

        _, leaving_points = walk_with_boundaries(grid, [entry], size, boundaries, n=n)
        assert len(leaving_points) == 4

        results[entry] = leaving_points

        for _, points in leaving_points.values():
            for p in points:
                if p in results:
                    continue
                explore.append(p)

    with open("21/cache.json", "w") as f:
        json.dump(
            {",".join(map(str, k)): {d: (vv[0], list(vv[1])) for d, vv in v.items()} for k, v in results.items()},
            f,
            indent=4,
        )

    return results


def find_expanson_pattern(
    boundary_steps: dict[V2, dict[str, tuple[int, list[V2]]]], start_points: list[V2]
) -> dict[tuple[frozenset[V2], str], list[tuple[tuple[frozenset[V2], str], int]]]:
    def _next_points(points: list[V2]):
        res = {}
        for d in DIRECTION_NAMES:
            all_outcomes = [boundary_steps[p][d] for p in points]
            best_outcome = min([o[0] for o in all_outcomes])
            res[d] = (best_outcome, frozenset([p for o in all_outcomes for p in o[1] if o[0] == best_outcome]))
        return res

    frontier = [(frozenset(start_points), "")]
    results = {}

    def _transform_key(key: tuple[frozenset[V2], str]) -> tuple[frozenset[V2], V2]:
        return (key[0], NAMES_TO_DIRECTIONS[key[1]])

    while frontier:
        current = frontier.pop(0)
        entry_points, direction = current
        key = _transform_key(current)

        if key in results:
            continue

        exits = {d: r for d, r in _next_points(list(entry_points)).items() if NO_RETURN[d] != direction}
        results[key] = [(_transform_key((points, d)), cost) for d, (cost, points) in exits.items()]

        for direction, (cost, points) in exits.items():
            next_v = (frozenset(points), direction)
            next_key = _transform_key(next_v)
            if next_key not in results:
                frontier.append(next_v)

    return results


fill_cache: dict[frozenset[V2], int] = {}


def count_fill(grid: set[V2], start: frozenset[V2]) -> int:
    if start in fill_cache:
        return fill_cache[start]

    explore: PriorityQueue[tuple[int, V2]] = PriorityQueue()

    for p in start:
        explore.put((0, p))

    seen = set()
    max_depth = 0

    while not explore.empty():
        depth, point = explore.get()
        if point in seen:
            continue
        seen.add(point)
        max_depth = max(max_depth, depth)

        for step1, step2 in product(DIRECTIONS, repeat=2):
            mid_point = (point[0] + step1[0], point[1] + step1[1])
            if mid_point not in grid:
                continue
            new_point = (mid_point[0] + step2[0], mid_point[1] + step2[1])

            if new_point not in grid:
                continue
            if new_point in seen:
                continue
            explore.put((depth + 2, new_point))

    fill_cache[start] = max_depth
    return max_depth


def solve(input_lines: list[str], n=26501365):
    grid = {(x, y) for y, line in enumerate(input_lines) for x, c in enumerate(line) if c != "#"}
    start = next((x, y) for y, line in enumerate(input_lines) for x, c in enumerate(line) if c == "S")
    size = (len(input_lines[0]), len(input_lines))
    boundaries = {
        "TOP": {(x, y) for x in range(size[0]) for y in (-1, -2)},
        "BOTTOM": {(x, y) for x in range(size[0]) for y in (size[1], size[1] + 1)},
        "LEFT": {(x, y) for x in (-1, -2) for y in range(size[1])},
        "RIGHT": {(x, y) for x in (size[0], size[0] + 1) for y in range(size[1])},
    }

    start_points = [(start[0] + d[0], start[1] + d[1]) for d in DIRECTIONS]
    # r = find_boundary_entries(grid, size, boundaries, start_points)
    # boundary_steps = load_boundaries()
    # expanson_points = find_expanson_pattern(boundary_steps, start_points)

    # frontier = PriorityQueue()
    # frontier.put((1, (0, 0), (frozenset(start_points), (0, 0)), count_fill(grid, frozenset(start_points))))

    # visited = {}

    # with open("21/.cache/fill_cache.json") as f:
    #     data = json.load(f)
    #     for points, val in data:
    #         fill_cache[frozenset(list(map(tuple, points)))] = val

    # while not frontier.empty():
    #     cost, p, leaving, fill = frontier.get()
    #     if visited.get(p, [math.inf])[0] <= cost:
    #         continue
    #     visited[p] = (cost, fill, leaving)

    #     for next_leaving, d_cost in expanson_points[leaving]:
    #         points, direction = next_leaving
    #         next_p = p[0] + direction[0], p[1] + direction[1]
    #         next_cost = cost + d_cost
    #         if next_cost > n:
    #             continue
    #         if visited.get(next_p, [math.inf])[0] <= next_cost:
    #             continue
    #         frontier.put((cost + d_cost, next_p, next_leaving, count_fill(grid, frozenset(points))))

    # SIZE = 10
    # for y in range(-SIZE, SIZE + 1):
    #     print(
    #         "".join(
    #             f"{s:10}"
    #             for s in [
    #                 f"{visited.get((x, y), [0])[0]}:{visited.get((x, y), [0, 0])[1]}" for x in range(-SIZE, SIZE + 1)
    #             ]
    #         )
    #     )

    diagonal_a_n = (n + 129) // 262  # Fills on 258
    diagonal_a_width = diagonal_a_n * 2 - 1
    diagonal_a_last = 1 + 2 * (diagonal_a_n - 1)
    diagonal_a_total = diagonal_a_n / 2 * (1 + diagonal_a_last)
    diagonal_a_entries = [[(130, 1), (129, 0)], [(0, 1), (1, 0)], [(1, 130), (0, 129)], [(129, 130), (130, 129)]]

    diagonal_b_n = (n - 1) // 262  # Fills on 260
    diagonal_b_width = diagonal_b_n * 2
    diagonal_b_last = 2 + 2 * (diagonal_b_n - 1)
    diagonal_b_total = diagonal_b_n / 2 * (2 + diagonal_b_last)
    diagonal_b_entries = [[(130, 130)], [(0, 130)], [(130, 0)], [(0, 0)]]

    d = max(diagonal_a_width, diagonal_b_width)
    diagonal_count = int(d * (d + 1) / 2)
    assert diagonal_a_total + diagonal_b_total == diagonal_count

    straight_a_n = (n + 195) // 262  # Fills on 194
    straight_a_width = straight_a_n * 2 - 1
    straight_a_entries = [
        [(0, 64), (1, 65), (0, 66)],
        [(130, 64), (130, 66), (129, 65)],
        [(66, 0), (64, 0), (65, 1)],
        [(66, 130), (64, 130), (65, 129)],
    ]

    straight_b_n = (n + 65) // 262  # Fills on 194
    straight_b_width = straight_b_n * 2
    straight_b_entries = [[(0, 65)], [(130, 65)], [(65, 0)], [(65, 130)]]

    straight_count = max(straight_a_width, straight_b_width)
    total_grid = 1 + diagonal_count * 4 + straight_count * 4

    # assert total_grid == len(visited)

    total = 0

    if n < 128:
        total += len(walk_limited(grid, start_points, n))
    else:
        total += 7407

    if n >= 133:
        diag_a_full = diagonal_a_total - diagonal_a_last
        total += diag_a_full * 4 * 7407
        diag_a_steps = n - ((diagonal_a_n * 262) - 129)
        diag_a_final_walks = [walk_limited(grid, p, diag_a_steps) for p in diagonal_a_entries]
        total += sum(map(len, diag_a_final_walks)) * diagonal_a_last
    if n >= 263:
        diag_b_full = diagonal_b_total - diagonal_b_last
        total += diag_b_full * 4 * 7481
        diag_b_steps = n - ((diagonal_b_n * 262) + 1)
        diag_b_final_walks = [walk_limited(grid, p, diag_b_steps) for p in diagonal_b_entries]
        total += sum(map(len, diag_b_final_walks)) * diagonal_b_last
    if n >= 67:
        straight_a_full = straight_a_n - 1
        total += straight_a_full * 4 * 7481
        straight_a_steps = n - ((straight_a_n * 262) - 195)
        straight_a_final_walks = [walk_limited(grid, p, straight_a_steps) for p in straight_a_entries]
        total += sum(map(len, straight_a_final_walks))
    if n >= 197:
        straight_b_full = straight_b_n - 1
        total += straight_b_full * 4 * 7407
        straight_b_steps = n - ((straight_b_n * 262) - 65)
        straight_b_final_walks = [walk_limited(grid, p, straight_b_steps) for p in straight_b_entries]
        total += sum(map(len, straight_b_final_walks))

    # seen = walk_unlimited(grid, start_points, size, n=n)

    # for tile in [(-2, 0), (-1, -1), (-1, 0), (-1, 1)]:
    #     tile_x, tile_y = tile[0] * 131, tile[1] * 131
    #     tile_seen = [(x - tile_x, y - tile_y) for x, y in seen if tile_x <= x < tile_x + 131 and tile_y <= y < tile_y + 131]
    #     print(tile)
    #     draw(input_lines, set(tile_seen))

    # assert len(seen) == total

    # seen, leaving_points = walk_from(grid, [(start[0] + d[0], start[1] + d[1]) for d in DIRECTIONS], size, boundaries)
    # seen, leaving_points = walk_from(grid, [start], size, boundaries)

    # seen, leaving_points = walk_from(grid, [(65, 1)], size, boundaries, n=66)
    # seen, leaving_points = walk_from(grid, [(65, 1)], size, boundaries, n=130)

    # draw(input_lines, seen)
    # return len(seen)
    return int(total)


def main():
    with open("21/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
