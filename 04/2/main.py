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
            return []
        return range(self._id + 1, self._id + count + 1)

    @property
    def id(self):
        return self._id


def solve(input_lines: list[str]):
    cards = {(c := Card(line)).id: c for line in input_lines}
    score_cache: dict[int, int] = {card_id: None for card_id in cards}

    win_count = 0

    def _get_win_count(card_id: int):
        if card_id not in score_cache:
            return 0
        if score_cache[card_id] is None:
            next_cards = cards[card_id].score
            score_cache[card_id] = 1 + sum(_get_win_count(next_card) for next_card in next_cards)
        return score_cache[card_id]

    for card_id in cards:
        win_count += _get_win_count(card_id)
    return win_count


def main():
    with open("04/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
