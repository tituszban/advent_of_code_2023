def solve(input_lines: list[str]):
    total = 0
    digits = {
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "0": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "zero": "0",
    }

    for line in input_lines:
        while not (digit := next((digit for digit in digits if line.startswith(digit)), None)):
            line = line[1:]
        first = digits[digit]
        while not (digit := next((digit for digit in digits if line.endswith(digit)), None)):
            line = line[:-1]
        last = digits[digit]
        total += int(first + last)
    return total


def main():
    with open("01/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
