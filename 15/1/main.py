def hash(s: str):
    value = 0
    for c in s:
        value += ord(c)
        value *= 17
        value %= 256
    return value


def solve(input_lines: list[str]):
    values = input_lines[0].split(",")

    return sum(map(hash, values))


def main():
    with open("15/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
