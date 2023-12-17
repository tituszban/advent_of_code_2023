import math
from queue import PriorityQueue


Point = tuple[int, int]
Step = tuple[int, int]

STEP_NORTH: Step = (0, -1)
STEP_SOUTH: Step = (0, 1)
STEP_WEST: Step = (-1, 0)
STEP_EAST: Step = (1, 0)

ALL_STEPS = (STEP_NORTH, STEP_SOUTH, STEP_WEST, STEP_EAST)

VALID_NEXT_STEPS: dict[Step, tuple[Step, ...]] = {
    STEP_NORTH: (STEP_NORTH, STEP_WEST, STEP_EAST),
    STEP_SOUTH: (STEP_SOUTH, STEP_WEST, STEP_EAST),
    STEP_WEST: (STEP_WEST, STEP_NORTH, STEP_SOUTH),
    STEP_EAST: (STEP_EAST, STEP_NORTH, STEP_SOUTH),
}


def _get_next_steps(prev_step: Step, prev_step_count: int) -> tuple[Step, ...]:
    valid_next_steps = VALID_NEXT_STEPS[prev_step]

    if prev_step_count < 3:
        return valid_next_steps

    return tuple(step for step in valid_next_steps if step != prev_step)


State = tuple[Point, Step, int]


def solve(input_lines: list[str]):
    grid: dict[Point, int] = {(x, y): int(c) for y, line in enumerate(input_lines) for x, c in enumerate(line)}
    frontier: PriorityQueue[tuple[int, int, State]] = PriorityQueue()
    frontier.put((0, 0, ((0, 0), STEP_SOUTH, 0)))
    seen_states: dict[State, int] = {}
    goal = (len(input_lines[0]) - 1, len(input_lines) - 1)

    while frontier:
        _, heat_loss, state = frontier.get()
        location, prev_step, prev_step_count = state

        valid_next_steps = _get_next_steps(prev_step, prev_step_count)

        for step in valid_next_steps:
            new_location = (location[0] + step[0], location[1] + step[1])
            if new_location not in grid:
                continue
            new_heat_loss = heat_loss + grid[new_location]

            if new_location == goal:
                return new_heat_loss

            next_state = (new_location, step, (1 if prev_step != step else prev_step_count + 1))

            if seen_states.get(next_state, math.inf) <= new_heat_loss:
                continue
            seen_states[next_state] = new_heat_loss

            fitness = new_heat_loss + abs(goal[0] - new_location[0]) + abs(goal[1] - new_location[1])
            frontier.put((fitness, new_heat_loss, next_state))


def main():
    with open("17/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
