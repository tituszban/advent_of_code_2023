from itertools import combinations


def expand(input_lines: list[str], n=1_000_000):
    def _expand(_original: list[str]):
        expanded_lines = []
        for line in _original:
            if all(c == "." for c in line):
                expanded_lines.append(n)
            else:
                expanded_lines.append(1)
        return expanded_lines

    rows = _expand(input_lines)
    cols = _expand(["".join(line) for line in zip(*input_lines)])

    return (rows, cols)


def solve(input_lines: list[str]):
    rows, cols = expand(input_lines)

    locations = [(x, y) for y, line in enumerate(input_lines) for x, c in enumerate(line) if c == "#"]

    comb = list(combinations(locations, 2))

    total = 0

    for a, b in comb:
        sub_total = 0
        for x in range(min(a[0], b[0]), max(a[0], b[0])):
            sub_total += cols[x]
        for y in range(min(a[1], b[1]), max(a[1], b[1])):
            sub_total += rows[y]
        total += sub_total

    return total


def main():
    with open("11/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
