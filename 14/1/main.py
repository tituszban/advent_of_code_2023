from dataclasses import dataclass


@dataclass
class Section:
    rock_count: int
    depth: int

    @property
    def total(self) -> int:
        return sum([self.depth - i for i in range(self.rock_count)])


def analyse_column(squares: list[str]) -> list[Section]:
    sections: list[Section] = []
    first_index = None
    rock_count = 0
    for i, c in enumerate(squares):
        if c == "#":
            if first_index is not None:
                sections.append(Section(rock_count, len(squares) - first_index))
                first_index = None
                rock_count = 0
            continue
        if first_index is None:
            first_index = i
        if c == "O":
            rock_count += 1
    if first_index is not None:
        sections.append(Section(rock_count, len(squares) - first_index))

    return [section for section in sections if section.rock_count > 0]


def solve(input_lines: list[str]):
    columns: list[list[str]] = list(zip(*input_lines))

    all_sections: list[Section] = []
    for column in columns:
        all_sections.extend(analyse_column(column))

    return sum([section.total for section in all_sections])


def main():
    with open("14/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
