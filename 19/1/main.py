import re


class Condition:
    def __init__(self, param: str, condition: str, value: int, result: str):
        self._param = param
        self._condition = condition
        self._value = value
        self._result = result

    @property
    def result(self):
        return self._result

    def check(self, xmas: dict[str, int]) -> bool:
        a = xmas[self._param]

        if self._condition == "<":
            return a < self._value
        if self._condition == ">":
            return a > self._value
        raise ValueError(f"Unknown condition: {self._condition}")


class PassthroughCondition(Condition):
    def __init__(self, result: str):
        self._result = result

    @property
    def result(self):
        return self._result

    def check(self, xmas: dict[str, int]) -> bool:
        return True


class Workflow:
    steps_parser = re.compile(r"((?P<param>[xmas])(?P<condition>[<>])(?P<value>\d+):)?(?P<result>[ARa-z]+)")

    def __init__(self, steps: str):
        self._conditions = [
            Condition(m.group("param"), m.group("condition"), int(m.group("value")), m.group("result"))
            if m.group("param")
            else PassthroughCondition(m.group("result"))
            for step in steps.split(",")
            if (m := self.steps_parser.match(step))
        ]
        assert len(self._conditions) == len(steps.split(","))

    def run(self, xmas: dict[str, int], dispatcher: "WorkflowDispatcher") -> bool:
        for condition in self._conditions:
            if condition.check(xmas):
                if condition.result == "A":
                    return True
                if condition.result == "R":
                    return False
                return dispatcher.dispatch(condition.result, xmas)
        raise Exception("No condition triggered")


class WorkflowDispatcher:
    workflow_parser = re.compile(r"^(?P<name>\w+)\{(?P<steps>.*)\}$")

    def __init__(self, workflow_lines: list[str]):
        self._workflows = {
            m.group("name"): Workflow(m.group("steps"))
            for line in workflow_lines
            if (m := self.workflow_parser.match(line))
        }
        assert len(self._workflows) == len(workflow_lines)

    def dispatch(self, workflow_name: str, xmas: dict[str, int]) -> bool:
        return self._workflows[workflow_name].run(xmas, self)


def split(input_lines: list[str]) -> tuple[list[str], list[str]]:
    workflows = []
    parts = []
    parts_flag = False
    for line in input_lines:
        if not line:
            parts_flag = True
        elif parts_flag:
            parts.append(line)
        else:
            workflows.append(line)
    return workflows, parts


parts_parser = re.compile(r"(?P<param>[xmas])=(?P<value>\d+)")


def solve(input_lines: list[str]):
    workflows, parts = split(input_lines)

    parts = [{m.group("param"): int(m.group("value")) for m in parts_parser.finditer(part)} for part in parts]

    dispatcher = WorkflowDispatcher(workflows)

    total = 0

    for part in parts:
        if dispatcher.dispatch("in", part):
            total += sum(part.values())

    return total


def main():
    with open("19/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
