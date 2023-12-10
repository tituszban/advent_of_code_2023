from main import *


def test_section_1():
    section = Section(
        [
            "seed-to-soil map:",
            "50 98 2",
            "52 50 48",
        ]
    )
    seed_range = Range(48, 110)
    sections = section.map_to_destination(seed_range)

    assert sections == [Range(48, 50), Range(52, 100), Range(50, 52), Range(100, 110)]


def test_section_2():
    section = Section(
        [
            "seed-to-soil map:",
            "50 98 2",
            "52 50 48",
        ]
    )
    seed_range = Range(60, 99)
    sections = section.map_to_destination(seed_range)

    assert sections == [
        Range(62, 100),
        Range(50, 51),
    ]


def test_section_3():
    section = Section(
        [
            "seed-to-soil map:",
            "50 98 2",
            "52 50 48",
        ]
    )
    seed_range = Range(60, 65)
    sections = section.map_to_destination(seed_range)

    assert sections == [
        Range(62, 67),
    ]


def test_example():
    input_lines = [
        "seeds: 79 14 55 13",
        "",
        "seed-to-soil map:",
        "50 98 2",
        "52 50 48",
        "",
        "soil-to-fertilizer map:",
        "0 15 37",
        "37 52 2",
        "39 0 15",
        "",
        "fertilizer-to-water map:",
        "49 53 8",
        "0 11 42",
        "42 0 7",
        "57 7 4",
        "",
        "water-to-light map:",
        "88 18 7",
        "18 25 70",
        "",
        "light-to-temperature map:",
        "45 77 23",
        "81 45 19",
        "68 64 13",
        "",
        "temperature-to-humidity map:",
        "0 69 1",
        "1 0 69",
        "",
        "humidity-to-location map:",
        "60 56 37",
        "56 93 4",
    ]
    assert solve(input_lines) == 46
