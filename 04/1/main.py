import re


class Card:
    card_re = re.compile(r"^Card\s+(?P<id>\d+):\s(?P<winning>[\d\s]+)\s\|\s(?P<nums>[\d\s]+)\s*$")

    def __init__(self, line: str):
        assert (m := self.card_re.match(line))
        self._id = int(m.group("id"))
        self._winning = set([int(n) for n in m.group("winning").split() if n])
        self._nums = [int(n) for n in m.group("nums").split() if n]

    @property
    def score(self):
        count = sum(1 for n in self._nums if n in self._winning)
        if count == 0:
            return 0
        return 2 ** (count - 1)


def solve(input_lines: list[str]):
    cards = [Card(line) for line in input_lines]
    return sum(card.score for card in cards)


def main():
    with open("04/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
