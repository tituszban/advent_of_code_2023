import re

Point = tuple[int, int]
Direction = tuple[int, int]

DIRECTIONS: dict[str, Direction] = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


def solve(input_lines: list[str]):
    parser_re = re.compile(r"^(?P<dir>[UDLR])\s(?P<count>\d+)\s\(#(?P<colour>[0-9a-f]{6})\)$")

    parsed = [parser_re.match(line) for line in input_lines]
    cursor = (0, 0)
    grid = {}
    for match in parsed:
        assert match
        direction = DIRECTIONS[match.group("dir")]
        for _ in range(int(match.group("count"))):
            cursor = (cursor[0] + direction[0], cursor[1] + direction[1])
            grid[cursor] = match.group("colour")

    fill_start = (1, 1)
    fill_queue: list[Point] = [fill_start]
    seen: set[Point] = set()
    while fill_queue:
        point = fill_queue.pop()
        grid[point] = "000000"

        for direction in DIRECTIONS.values():
            new_point = (point[0] + direction[0], point[1] + direction[1])
            if new_point not in grid and new_point not in seen:
                seen.add(new_point)
                fill_queue.append(new_point)

    return len(grid)


def main():
    with open("18/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
