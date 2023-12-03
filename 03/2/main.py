class Number:
    def __init__(self, n: str) -> None:
        self._n = int(n)
        self._len = len(n)

    @property
    def range(self):
        return range(self._len)
    
    @property
    def n(self):
        return self._n

def build_grid(input_lines: list[str]):
    grid = []
    for line in input_lines:
        acc = ""
        row = []
        for c in line:
            if c in "0123456789":
                acc += c
            else:
                if any(acc):
                    n = Number(acc)
                    for _ in n.range:
                        row.append(n)
                acc = ""
                row.append(None)
        if any(acc):
            n = Number(acc)
            for _ in n.range:
                row.append(n)
        assert len(row) == len(line)
        grid.append(row)

    return grid


def solve(input_lines: list[str]):
    grid = build_grid(input_lines)

    sum_product = 0
    for i, line in enumerate(input_lines):
        for j, c in enumerate(line):
            if c != "*":
                continue
            numbers = set()
            for i_o in [-1, 0, 1]:
                for j_o in [-1, 0, 1]:
                    if (v := grid[i + i_o][j + j_o]) is not None:
                        numbers.add(v)
            if len(numbers) == 2:
                numbers_l = list(numbers)
                sum_product += numbers_l[0].n * numbers_l[1].n

    return sum_product
        


def main():
    with open("03/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))
    # test_input = [
    #     "467..114..",
    #     "...*......",
    #     "..35..633.",
    #     "......#...",
    #     "617*......",
    #     ".....+.58.",
    #     "..592.....",
    #     "......755.",
    #     "...$.*....",
    #     ".664.598..",
    # ]

    print(solve(test_input))


if __name__ == "__main__":
    main()
