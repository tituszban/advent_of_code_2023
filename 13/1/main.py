from typing import Optional


def split_patterns(input_lines: list[str]):
    patterns: list[list[str]] = []
    pattern: list[str] = []
    for line in input_lines:
        if line == "":
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    patterns.append(pattern)
    return patterns


def rotate_pattern(pattern: list[str]) -> list[str]:
    return list(map(lambda line: "".join(line), zip(*pattern)))


def do_reflect(top: list[str], bottom: list[str]) -> bool:
    return all(t == b for t, b in zip(reversed(top), bottom))


def find_pattern_reflection(pattern: list[str]) -> Optional[int]:
    for i in range(1, len(pattern)):
        if do_reflect(pattern[:i], pattern[i:]):
            return i


def solve(input_lines: list[str]):
    patterns = split_patterns(input_lines)

    total = 0
    for pattern in patterns:
        v = find_pattern_reflection(pattern)
        if v is not None:
            total += v * 100
            continue
        h = find_pattern_reflection(rotate_pattern(pattern))
        assert h is not None
        total += h

    return total


def main():
    with open("13/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
