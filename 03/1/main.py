import numpy as np
from scipy.signal import convolve2d

def get_symbol_adjacent(input_lines: list[str]):
    symbols = np.array([[0 if c in "0123456789." else 1 for c in line] for line in input_lines])
    kernel = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ])
    return convolve2d(symbols, kernel, mode="same", boundary="fill", fillvalue=0)


def solve(input_lines: list[str]):
    symbol_adjacent = get_symbol_adjacent(input_lines)
    numbers = []
    for i, line in enumerate(input_lines):
        acc = ""
        had_symbol = False
        for j, c in enumerate(line):
            if c in "0123456789":
                if symbol_adjacent[i][j] != 0:
                    had_symbol = True
                acc += c
            else:
                if had_symbol:
                    numbers.append(acc)
                acc = ""
                had_symbol = False
        if had_symbol:
            numbers.append(acc)

    return sum(map(int, numbers))
        


def main():
    with open("03/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
