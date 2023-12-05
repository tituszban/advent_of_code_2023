from functools import reduce


class Section:
    def __init__(self, lines: list[str]):
        self._source, _, self._destination = lines[0].split()[0].split("-")
        self._ranges = sorted([tuple(map(int, line.split())) for line in lines[1:]], key=lambda r: r[1])

    def map_to_destination(self, value: int):
        for dest, source, length in self._ranges:
            if source <= value < source + length:
                return value - source + dest
        return value


def solve(input_lines: list[str]):
    seeds = list(map(int, input_lines[0].split(": ")[1].split()))

    def reduce_sections(acc: list[list[str]], line: str):
        if line == "":
            acc.append([])
        else:
            acc[-1].append(line)
        return acc

    sections = list(map(Section, reduce(reduce_sections, input_lines[2:], [[]])))

    def map_seed(_seed: int):
        return reduce(lambda seed, s: s.map_to_destination(seed), sections, _seed)

    return min(map(map_seed, seeds))


def main():
    with open("05/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
