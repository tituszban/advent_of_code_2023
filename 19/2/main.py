from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import reduce
import re


MIN_VALUE = 1
MAX_VALUE = 4000


class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def intersect(self, other: "Range") -> "Range":
        return Range(max(self.start, other.start), min(self.end, other.end))

    def count(self) -> int:
        if self.end > self.start:
            return self.end - self.start + 1
        return 0

    @classmethod
    def empty(cls) -> "Range":
        return cls(MAX_VALUE, MIN_VALUE)

    @classmethod
    def full(cls) -> "Range":
        return cls(MIN_VALUE, MAX_VALUE)

    def __repr__(self) -> str:
        return f"{self.start}-{self.end} ({self.count()})"


class ConditionABC(ABC):
    @abstractmethod
    def __invert__(self) -> "ConditionABC":
        raise NotImplementedError

    @abstractmethod
    def __and__(self, other: "ConditionABC") -> "ConditionABC":
        raise NotImplementedError

    @abstractmethod
    def __or__(self, other: "ConditionABC") -> "ConditionABC":
        raise NotImplementedError

    @abstractmethod
    def apply(self, xmas: dict[str, Range]) -> dict[str, Range]:
        raise NotImplementedError


class AndCondition(ConditionABC):
    def __init__(self, left: ConditionABC, right: ConditionABC):
        self.left = left
        self.right = right

    def __invert__(self) -> ConditionABC:
        return OrCondition(~self.left, ~self.right)

    def __and__(self, other: ConditionABC) -> ConditionABC:
        if isinstance(other, (YesCondition, NoCondition)):
            return other & self
        return AndCondition(self, other)

    def __or__(self, other: ConditionABC) -> ConditionABC:
        if isinstance(other, (YesCondition, NoCondition)):
            return other | self
        return OrCondition(self, other)

    def __repr__(self) -> str:
        return f"({self.left} & {self.right})"

    def apply(self, xmas: dict[str, Range]) -> dict[str, Range]:
        return self.left.apply(self.right.apply(xmas))


class OrCondition(ConditionABC):
    def __init__(self, left: ConditionABC, right: ConditionABC):
        self.left = left
        self.right = right

    def __invert__(self) -> ConditionABC:
        return AndCondition(~self.left, ~self.right)

    def __and__(self, other: ConditionABC) -> ConditionABC:
        if isinstance(other, (YesCondition, NoCondition)):
            return other & self
        return AndCondition(self, other)

    def __or__(self, other: ConditionABC) -> ConditionABC:
        if isinstance(other, (YesCondition, NoCondition)):
            return other | self
        return OrCondition(self, other)

    def __repr__(self) -> str:
        return f"({self.left} | {self.right})"

    def apply(self, xmas: dict[str, Range]) -> dict[str, Range]:
        raise NotImplementedError


class Condition(ConditionABC):
    def __init__(self, param: str, condition: str, value: int):
        self.param = param
        self.condition = condition
        self.value = value

    def __invert__(self) -> "Condition":
        if self.condition == "<":
            return Condition(self.param, ">", self.value - 1)
        if self.condition == ">":
            return Condition(self.param, "<", self.value + 1)
        raise ValueError(f"Unknown condition: {self.condition}")

    def __and__(self, other: ConditionABC) -> ConditionABC:
        if isinstance(other, (YesCondition, NoCondition)):
            return other & self
        return AndCondition(self, other)

    def __or__(self, other: ConditionABC) -> ConditionABC:
        if isinstance(other, (YesCondition, NoCondition)):
            return other | self
        return OrCondition(self, other)

    def __repr__(self) -> str:
        return f"({self.param} {self.condition} {self.value})"

    @property
    def range(self) -> Range:
        if self.condition == "<":
            return Range(MIN_VALUE, self.value - 1)
        if self.condition == ">":
            return Range(self.value + 1, MAX_VALUE)
        raise ValueError(f"Unknown condition: {self.condition}")

    def apply(self, xmas: dict[str, Range]) -> dict[str, Range]:
        return {**xmas, self.param: xmas[self.param].intersect(self.range)}


class YesCondition(ConditionABC):
    def __invert__(self):
        return NoCondition()

    def __and__(self, other: ConditionABC) -> ConditionABC:
        return other

    def __or__(self, other: ConditionABC) -> ConditionABC:
        return YesCondition()

    def __repr__(self) -> str:
        return "ACCEPT"

    def apply(self, xmas: dict[str, Range]) -> dict[str, Range]:
        raise NotImplementedError


class NoCondition(ConditionABC):
    def __invert__(self):
        return YesCondition()

    def __and__(self, other: ConditionABC) -> ConditionABC:
        return NoCondition()

    def __or__(self, other: ConditionABC) -> ConditionABC:
        return other

    def __repr__(self) -> str:
        return "REJECT"

    def apply(self, xmas: dict[str, Range]) -> dict[str, Range]:
        return {k: Range.empty() for k in xmas}


@dataclass
class WorkflowStep:
    condition: ConditionABC
    outcome: str


class Workflow:
    steps_parser = re.compile(r"((?P<param>[xmas])(?P<condition>[<>])(?P<value>\d+):)?(?P<result>[ARa-z]+)")

    def __init__(self, steps: str):
        self._steps = [
            WorkflowStep(Condition(m.group("param"), m.group("condition"), int(m.group("value"))), m.group("result"))
            if m.group("param")
            else WorkflowStep(YesCondition(), m.group("result"))
            for step in steps.split(",")
            if (m := self.steps_parser.match(step))
        ]
        assert len(self._steps) == len(steps.split(","))

    def run(self, dispatcher: "WorkflowDispatcher") -> list[ConditionABC]:
        def _get_outcome(step: WorkflowStep):
            if step.outcome == "A":
                return [YesCondition()]
            if step.outcome == "R":
                return [NoCondition()]
            return dispatcher.dispatch(step.outcome)

        conditions = []
        pre_conditions = []
        for step in self._steps:
            outcome = _get_outcome(step)
            for o in outcome:
                r = step.condition & o
                for c in pre_conditions:
                    r = c & r
                conditions.append(r)
            pre_conditions.append(~step.condition)

        return conditions


class WorkflowDispatcher:
    workflow_parser = re.compile(r"^(?P<name>\w+)\{(?P<steps>.*)\}$")

    def __init__(self, workflow_lines: list[str]):
        self._workflows = {
            m.group("name"): Workflow(m.group("steps"))
            for line in workflow_lines
            if (m := self.workflow_parser.match(line))
        }
        assert len(self._workflows) == len(workflow_lines)
        self._cache = {}

    def dispatch(self, workflow_name: str) -> list[ConditionABC]:
        if workflow_name not in self._cache:
            self._cache[workflow_name] = self._workflows[workflow_name].run(self)
        return self._cache[workflow_name]


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

    conditions = dispatcher.dispatch("in")

    xmas = {
        "x": Range.full(),
        "m": Range.full(),
        "a": Range.full(),
        "s": Range.full(),
    }

    total = 0

    for condition in conditions:
        result = condition.apply(xmas)
        total += reduce(lambda acc, r: acc * r.count(), result.values(), 1)

    return total


def main():
    with open("19/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
