from main import solve


def test_main():
    assert solve(
        [
            "-L|F7",
            "7S-7|",
            "L|7||",
            "-L-J|",
            "L|-JF",
        ]
    ) == 4
