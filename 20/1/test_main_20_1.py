from main import solve


def test_main_example1():
    assert solve(
        [
            "broadcaster -> a, b, c",
            "%a -> b",
            "%b -> c",
            "%c -> inv",
            "&inv -> a",
        ]
    ) == 32000000


def test_main_example2():
    assert solve(
        [
            "broadcaster -> a",
            "%a -> inv, con",
            "&inv -> b",
            "%b -> con",
            "&con -> output",
        ]
    ) == 11687500
