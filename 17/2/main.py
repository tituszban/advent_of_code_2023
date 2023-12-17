from collections import defaultdict
import math
from queue import PriorityQueue
from typing import Mapping, Union


Point = tuple[int, int]
Step = tuple[int, int]

STEP_NORTH: Step = (0, -1)
STEP_SOUTH: Step = (0, 1)
STEP_WEST: Step = (-1, 0)
STEP_EAST: Step = (1, 0)

ALL_STEPS = (STEP_NORTH, STEP_SOUTH, STEP_WEST, STEP_EAST)

VALID_NEXT_DIRECTION: dict[Step, tuple[Step, ...]] = {
    STEP_NORTH: (STEP_WEST, STEP_EAST),
    STEP_SOUTH: (STEP_WEST, STEP_EAST),
    STEP_WEST: (STEP_NORTH, STEP_SOUTH),
    STEP_EAST: (STEP_NORTH, STEP_SOUTH),
}
MIN_STEPS = 4
MAX_STEPS = 10


State = tuple[Point, Step]


def solve(input_lines: list[str]):
    grid: dict[Point, int] = {(x, y): int(c) for y, line in enumerate(input_lines) for x, c in enumerate(line)}
    frontier: PriorityQueue[tuple[int, int, State]] = PriorityQueue()
    frontier.put((0, 0, ((0, 0), STEP_SOUTH)))
    frontier.put((0, 0, ((0, 0), STEP_EAST)))
    seen_states: Mapping[State, Union[int, float]] = defaultdict(lambda: math.inf)
    goal = (len(input_lines[0]) - 1, len(input_lines) - 1)

    while not frontier.empty():
        _, heat_loss, state = frontier.get()
        location, prev_step = state

        if location == goal:
            return heat_loss

        if seen_states[state] < heat_loss:
            continue

        for direction in VALID_NEXT_DIRECTION[prev_step]:
            new_heat_loss = heat_loss
            for dist in range(1, MAX_STEPS + 1):
                new_location = (location[0] + direction[0] * dist, location[1] + direction[1] * dist)
                if (point_loss := grid.get(new_location)) is None:
                    break
                new_heat_loss += point_loss
                if dist < MIN_STEPS:
                    continue

                next_state = (new_location, direction)

                if seen_states[next_state] <= new_heat_loss:
                    continue
                seen_states[next_state] = new_heat_loss

                new_fitness = new_heat_loss + abs(goal[0] - new_location[0]) + abs(goal[1] - new_location[1])
                frontier.put((new_fitness, new_heat_loss, next_state))


def main():
    with open("17/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
