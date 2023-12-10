from math import ceil, floor

e = 10**-10


def solve_quadratic(a: float, b: float, c: float):
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        raise ValueError("No real solutions")

    x1 = (-b + discriminant**0.5) / (2 * a)
    x2 = (-b - discriminant**0.5) / (2 * a)
    return x1, x2


def solve(input_lines: list[str]):
    times = [int(v) for v in input_lines[0].split()[1:] if v]
    dists = [int(v) for v in input_lines[1].split()[1:] if v]

    range_product = 1

    for time, dist in zip(times, dists):
        roots = solve_quadratic(-1, time, -dist)
        range_product *= floor(roots[1] - e) - ceil(roots[0] + e) + 1
    return range_product


def main():
    with open("06/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
