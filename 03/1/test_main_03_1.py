from main import solve

test_input = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]

expected_result = 4361


def test_solve():
    actual_result = solve(test_input)
    assert actual_result == expected_result
