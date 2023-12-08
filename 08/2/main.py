from math import lcm
from itertools import cycle


class Node:
    def __init__(self, line: str):
        self._id, lr = line.split(" = ")
        self._left, self._right = lr[1:-1].split(", ")

    def get_next(self, d: str):
        if d == "L":
            return self._left
        if d == "R":
            return self._right
        raise Exception(f"Invalid direction: {d}")

    @property
    def id(self):
        return self._id


def simulate(directions: str, nodes: dict[str, Node]):
    current = [node_id for node_id in nodes if node_id.endswith("A")]
    for i, inst in enumerate(cycle(directions)):
        prev = list(current)
        current = [
            nodes[node_id].get_next(inst)
            for node_id in current
        ]
        yield (i + 1, prev, current)


def solve(input_lines: list[str]):
    directions = input_lines[0]

    nodes = {node.id: node for line in input_lines[2:] if (node := Node(line))}

    current = [node_id for node_id in nodes if node_id.endswith("A")]

    loop_checks: dict[int, dict[tuple[int, str], tuple[int, str]]] = {i: {} for i in range(len(current))}
    first_z_index: dict[int, int] = {}

    loop_heads: dict[int, tuple[int, str]] = {}

    for i, prev, current in simulate(directions, nodes):
        for j, node_id in enumerate(current):
            from_key = ((i - 1) % len(directions), prev[j])
            to_key = (i % len(directions), node_id)

            if to_key in loop_checks[j] and node_id.endswith("Z"):
                loop_heads[j] = to_key
            loop_checks[j][from_key] = to_key

            if node_id.endswith("Z"):
                first_z_index[j] = i

        if len(loop_heads) == len(current):
            break

    loops = {}

    for j, head in loop_heads.items():
        loop_check = loop_checks[j]
        length = 0
        current = head
        while True:
            current = loop_check[current]
            length += 1
            if current == head:
                break
        loops[j] = length

    return lcm(*loops.values())


def main():
    with open("08/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
