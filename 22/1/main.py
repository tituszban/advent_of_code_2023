V2 = tuple[int, int]


class Brick:
    def __init__(self, line: str):
        v1, v2 = line.split("~")
        v1s, v2s = tuple(map(int, v1.split(","))), tuple(map(int, v2.split(",")))
        self._a = min(v1s, v2s, key=sum)
        self._b = max(v1s, v2s, key=sum)
        assert sum(self._a) <= sum(self._b)
        self._supported_by: set["Brick"] = set()
        self._supporting: set["Brick"] = set()

    @property
    def starting_z(self):
        return self._b[2]

    def get_values(self) -> tuple[list[V2], int]:
        values: list[V2] = []
        for x in range(self._a[0], self._b[0] + 1):
            for y in range(self._a[1], self._b[1] + 1):
                values.append((x, y))
        z = self._b[2] - self._a[2] + 1

        return values, z

    def add_supported_by(self, bricks: list["Brick"]):
        for b in bricks:
            self._supported_by.add(b)

    def add_supporting(self, brick: "Brick"):
        self._supporting.add(brick)

    def __repr__(self) -> str:
        return f"Brick({self._a}, {self._b})"

    @property
    def supporting(self) -> set["Brick"]:
        return self._supporting

    @property
    def supported_by(self) -> set["Brick"]:
        return self._supported_by

    def __hash__(self) -> int:
        return hash((self._a, self._b))


def solve(input_lines: list[str]):
    bricks = sorted([Brick(line) for line in input_lines], key=lambda b: b.starting_z)

    grid: dict[V2, tuple[int, "Brick"]] = {}

    for brick in bricks:
        area, height = brick.get_values()
        max_height = max(grid.get(p, [0])[0] for p in area)
        supported_by = [
            s for p in area if grid.get(p, [0])[0] == max_height and (s := grid.get(p, [0, None])[1]) is not None
        ]
        brick.add_supported_by(supported_by)
        for s in supported_by:
            s.add_supporting(brick)
        for p in area:
            grid[p] = (max_height + height, brick)

    can_be_removed = set()

    for brick in bricks:
        if all(len(b.supported_by) > 1 for b in brick.supporting):
            can_be_removed.add(brick)

    return len(can_be_removed)


def main():
    with open("22/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
