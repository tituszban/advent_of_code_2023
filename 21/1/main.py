from itertools import product
from queue import PriorityQueue

DIRECTIONS = (
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
)

def draw(input_lines: list[str], seen: set[tuple[int, int]]):
    print("====")
    for y, line in enumerate(input_lines):
        print(''.join("O" if (x, y) in seen else c for x, c in enumerate(line)))

def solve(input_lines: list[str], n = 64):
    grid = {(x, y) for y, line in enumerate(input_lines) for x, c in enumerate(line) if c != "#"}
    start = next((x, y) for y, line in enumerate(input_lines) for x, c in enumerate(line) if c == "S")

    explore: PriorityQueue[tuple[int, tuple[int, int]]] = PriorityQueue()
    explore.put((0, start))
    seen = set()

    while not explore.empty():
        depth, point = explore.get()
        if point in seen:
            continue
        seen.add(point)
        
        for step1, step2 in product(DIRECTIONS, repeat=2):
            mid_point = (point[0] + step1[0], point[1] + step1[1])
            if mid_point not in grid:
                continue
            new_point = (mid_point[0] + step2[0], mid_point[1] + step2[1])
            if new_point not in grid:
                continue
            if new_point in seen:
                continue
            if depth + 2 > n:
                continue
            explore.put((depth + 2, new_point))

    draw(input_lines, seen)
    return len(seen)




def main():
    with open("21/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
