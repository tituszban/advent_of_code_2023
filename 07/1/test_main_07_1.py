from main import solve


def test_main():
    assert (
        solve(
            [
                "32T3K 765",
                "T55J5 684",
                "KK677 28",
                "KTJJT 220",
                "QQQJA 483",
            ]
        )
        == 6440
    )
