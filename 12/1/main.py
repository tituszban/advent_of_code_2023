from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    spaces: int
    children: list["Node"]
    value_after: Optional[int]


def find_possible_patterns(count: list[int], limit: int) -> list[Node]:
    spaces_total = limit - sum(count)
    slot_count = len(count) + 1

    def _get_nodes(_total: int, _slots: int) -> list[Node]:
        if _slots == 1:
            return [Node(_total, [], None)]

        nodes = []

        for i in range(0 if _slots == slot_count else 1, _total - _slots + 3):
            nodes += [Node(i, _get_nodes(_total - i, _slots - 1), count[slot_count - _slots])]

        return nodes

    return _get_nodes(spaces_total, slot_count)


def count_valid_patterns(nodes: list[Node], pattern: str) -> int:
    total = 0
    for node in nodes:
        if not all(c in (".", "?") for c in pattern[: node.spaces]):
            continue
        if node.value_after is None:
            assert not any(node.children)
            total += 1
            continue
        if not all(c in ("#", "?") for c in pattern[node.spaces : node.spaces + node.value_after]):
            continue
        total += count_valid_patterns(node.children, pattern[node.spaces + node.value_after :])

    return total


def find_pattern_counts(counts: list[int], pattern: str) -> int:
    limit = len(pattern)

    patterns = find_possible_patterns(counts, limit)
    valid_count = count_valid_patterns(patterns, pattern)

    return valid_count


def solve(input_lines: list[str]):
    total = 0

    for line in input_lines:
        pattern, c = line.split()
        counts = list(map(int, c.split(",")))

        total += find_pattern_counts(counts, pattern)

    return total


def main():
    with open("12/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
