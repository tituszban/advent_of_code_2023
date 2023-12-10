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


def solve(input_lines: list[str]):
    directions = input_lines[0]

    nodes = {node.id: node for line in input_lines[2:] if (node := Node(line))}

    current = "AAA"
    goal = "ZZZ"
    for i, inst in enumerate(cycle(directions)):
        current = nodes[current].get_next(inst)
        if current == goal:
            return i + 1


def main():
    with open("08/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
