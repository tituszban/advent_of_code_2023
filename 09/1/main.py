class Sequence:
    def __init__(self, values: list[int]):
        self._values = values

    @classmethod
    def from_input(cls, line: str) -> "Sequence":
        return cls(list(map(int, line.split())))

    def derivative(self) -> "Sequence":
        return Sequence([v - p for v, p in zip(self._values[1:], self._values)])

    def extend(self) -> "Sequence":
        d_v = self.derivative()
        if all([v == 0 for v in d_v]):
            return Sequence([*self._values, self.last])
        e = d_v.extend().last
        return Sequence([*self._values, self.last + e])

    def __iter__(self):
        return iter(self._values)

    @property
    def last(self) -> int:
        return self._values[-1]


def solve(input_lines: list[str]):
    return sum(Sequence.from_input(line).extend().last for line in input_lines)


def main():
    with open("09/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
