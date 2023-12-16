import re


def hash(s: str):
    value = 0
    for c in s:
        value += ord(c)
        value *= 17
        value %= 256
    return value


def solve(input_lines: list[str]):
    inst_re = re.compile(r"^(?P<label>\w+)(?P<inst>[-=])(?P<num>\d+)?$")
    values = list(map(inst_re.match, input_lines[0].split(",")))

    boxes: dict[int, list[tuple[str, int]]] = {i: [] for i in range(256)}

    for value in values:
        assert value
        label = value.group("label")
        inst = value.group("inst")
        box = hash(label)

        lenses_by_key = {v[0]: i for i, v in enumerate(boxes[box])}

        if inst == "-":
            if label in lenses_by_key:
                boxes[box].pop(lenses_by_key[label])
        elif inst == "=":
            num = value.group("num")
            if label in lenses_by_key:
                boxes[box][lenses_by_key[label]] = (label, int(num))
            else:
                boxes[box].append((label, int(num)))

    return sum((box + 1) * (i + 1) * lense[1] for box, lenses in boxes.items() for i, lense in enumerate(lenses))


def main():
    with open("15/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
