def solve(input_lines: list[str]):
    total = 0
    for line in input_lines:
        while not line[0].isdigit():
            line = line[1:]
        while not line[-1].isdigit():
            line = line[:-1]
        total += int(line[0] + line[-1])
    return total


def main():
    with open("01/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
