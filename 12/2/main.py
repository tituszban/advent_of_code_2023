from functools import cache
from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    counts: tuple[int, ...]
    pattern: str
    is_first: bool = True


@cache
def count_children(node: Node) -> int:
    pattern = node.pattern
    counts = node.counts

    spaces_total = len(pattern) - sum(counts)
    slot_count = len(counts) + 1

    if slot_count == 1:
        return 1 if all(c in (".", "?") for c in pattern) else 0

    total = 0
    next_value = counts[0]
    for i in range(0 if node.is_first else 1, spaces_total - slot_count + 3):
        if i != 0 and pattern[i - 1] not in (".", "?"):
            break
        if not all(c in ("#", "?") for c in pattern[i : i + next_value]):
            continue
        if i + next_value < len(pattern) and pattern[i + next_value] not in (".", "?"):
            continue
        total += count_children(Node(counts[1:], pattern[i + next_value :], False))
    return total


def find_pattern_counts(counts: tuple[int, ...], pattern: str) -> int:
    valid_count = count_children(Node(counts, pattern))

    return valid_count


def solve(input_lines: list[str], n: int = 5):
    total = 0

    for line in input_lines:
        pattern, c = line.split()
        counts = list(map(int, c.split(",")))

        pattern = "?".join([pattern for _ in range(n)])
        counts = [c for _ in range(n) for c in counts]

        total += find_pattern_counts(tuple(counts), pattern)

    return total


def main():
    with open("12/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
