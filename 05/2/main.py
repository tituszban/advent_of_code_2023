from dataclasses import dataclass
from functools import reduce


@dataclass
class Range:
    start: int
    end: int

    def offset(self, offset: int):
        return Range(self.start + offset, self.end + offset)

    def trim(self, start: int):
        return Range(start, self.end)


class Section:
    def __init__(self, lines: list[str]):
        self._source, _, self._destination = lines[0].split()[0].split("-")
        self._ranges = sorted([tuple(map(int, line.split())) for line in lines[1:]], key=lambda r: r[1])

    def map_to_destination(self, value: Range) -> list[Range]:
        mapped_ranges = []
        ranges = list(self._ranges)

        while any(ranges):
            dest, source, length = ranges[0]
            if source >= value.end:
                mapped_ranges.append(value)
                break
            if source > value.start:
                mapped_ranges.append(Range(value.start, source))
                value = value.trim(source)
                continue
            if source + length <= value.start:
                ranges.pop(0)
                continue
            if source + length >= value.end:
                mapped_ranges.append(value.offset(dest - source))
                break

            mapped_ranges.append(Range(value.start, source + length).offset(dest - source))
            value = value.trim(source + length)
            ranges.pop(0)
        if not any(ranges):
            mapped_ranges.append(value)

        return mapped_ranges


def solve(input_lines: list[str]):
    seeds = list(map(int, input_lines[0].split(": ")[1].split()))
    seed_ranges = [Range(start, start + length) for start, length in zip(seeds[::2], seeds[1::2])]

    def reduce_sections(acc: list[list[str]], line: str):
        if line == "":
            acc.append([])
        else:
            acc[-1].append(line)
        return acc

    sections = list(map(Section, reduce(reduce_sections, input_lines[2:], [[]])))

    def map_seed(_seed_range: Range):
        return reduce(
            lambda seeds, s: [dest for seed in seeds for dest in s.map_to_destination(seed)], sections, [_seed_range]
        )

    return min([seed.start for seeds in map(map_seed, seed_ranges) for seed in seeds])


def main():
    with open("05/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
