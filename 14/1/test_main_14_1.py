from main import solve


def test_main():
    assert (
        solve(
            [
                "O....#....",
                "O.OO#....#",
                ".....##...",
                "OO.#O....O",
                ".O.....O#.",
                "O.#..O.#.#",
                "..O..#O..O",
                ".......O..",
                "#....###..",
                "#OO..#....",
            ]
        )
        == 136
    )
