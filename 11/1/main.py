from itertools import combinations


def expand(input_lines: list[str]):
    def _expand(_original: list[str]):
        expanded_lines = []
        for line in _original:
            expanded_lines.append(line)
            if all(c == "." for c in line):
                expanded_lines.append(line)
        return expanded_lines

    expanded = _expand(input_lines)

    return _expand(["".join(line) for line in zip(*expanded)])


def solve(input_lines: list[str]):
    expanded = expand(input_lines)

    locations = [(x, y) for y, line in enumerate(expanded) for x, c in enumerate(line) if c == "#"]

    comb = list(combinations(locations, 2))

    return sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in comb)


def main():
    with open("11/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
