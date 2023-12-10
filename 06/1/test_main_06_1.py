from main import solve


def test_main():
    assert (
        solve(
            [
                "Time:      7  15   30",
                "Distance:  9  40  200",
            ]
        )
        == 288
    )
