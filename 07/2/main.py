from functools import reduce


def calculate_rank(cards: str):
    count_by_type = sorted(
        reduce(
            lambda acc, c: {**acc, c: acc.get(c, 0) + 1},
            cards, {}).items(),
        key=lambda kv: kv[1], reverse=True)
    return (
        6 if count_by_type[0][1] == 5 else
        5 if count_by_type[0][1] == 4 else
        4 if count_by_type[0][1] == 3 and count_by_type[1][1] == 2 else
        3 if count_by_type[0][1] == 3 else
        2 if count_by_type[0][1] == 2 and count_by_type[1][1] == 2 else
        1 if count_by_type[0][1] == 2 else
        0
    )


def calculate_rank_with_joker(cards: str):
    if cards == "JJJJJ":
        return 6

    non_joker_cards = list(set(cards.replace("J", "")))

    def generate_possible_hands(_cards: str):
        if len(_cards) == 1:
            if _cards[0] == "J":
                return non_joker_cards
            return [_cards[0]]

        rest_of_hands = generate_possible_hands(_cards[1:])

        if _cards[0] != "J":
            return [_cards[0] + h for h in rest_of_hands]

        return [c + h for h in rest_of_hands for c in non_joker_cards]

    return max([calculate_rank(h) for h in generate_possible_hands(cards)])


class Hand:
    cards_ranked = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']

    def __init__(self, cards: str) -> None:
        self._cards = cards
        self._ranks = [self.cards_ranked.index(c) for c in cards]
        self._rank = calculate_rank_with_joker(self._cards)

    @property
    def sorting_key(self):
        return [self._rank, *self._ranks]

    def __repr__(self) -> str:
        return f"Hand({self._cards})"


def solve(input_lines: list[str]):
    hands = [
        (Hand(sp[0]), int(sp[1]))
        for line in input_lines
        if (sp := line.split())
    ]
    ranked = sorted(hands, key=lambda h: h[0].sorting_key)
    return sum([(i + 1) * hand[1] for i, hand in enumerate(ranked)])


def main():
    with open("07/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
