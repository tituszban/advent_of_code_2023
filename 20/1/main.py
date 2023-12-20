from dataclasses import dataclass
import enum
from abc import ABC, abstractmethod


class Pulse(enum.Enum):
    low = "low"
    high = "high"

    def __invert__(self):
        if self == Pulse.low:
            return Pulse.high
        else:
            return Pulse.low


@dataclass
class DirectedPulse:
    destination: str
    pulse: Pulse
    source: str

    def __repr__(self) -> str:
        return f"{self.source} -{self.pulse.value}-> {self.destination}"


class Node(ABC):
    def __init__(self, node: str, input_nodes: list[str], output_nodes: list[str]):
        self._node = node
        self._input_nodes = input_nodes
        self._output_nodes = output_nodes

    @abstractmethod
    def apply(self, pulse: DirectedPulse) -> list[DirectedPulse]:
        raise NotImplementedError

    def _dispatch(self, pulse: Pulse) -> list[DirectedPulse]:
        return [DirectedPulse(node, pulse, self._node) for node in self._output_nodes]


class FlipFlopNode(Node):
    def __init__(self, node: str, input_nodes: list[str], output_nodes: list[str]):
        super().__init__(node, input_nodes, output_nodes)
        self._state = Pulse.low

    def apply(self, pulse: DirectedPulse):
        if pulse.pulse == Pulse.high:
            return []
        self._state = ~self._state
        return self._dispatch(self._state)


class ConjunctionNode(Node):
    def __init__(self, node: str, input_nodes: list[str], output_nodes: list[str]):
        super().__init__(node, input_nodes, output_nodes)
        self._state = {node: Pulse.low for node in input_nodes}

    def apply(self, pulse: DirectedPulse) -> list[DirectedPulse]:
        assert pulse.source in self._state
        self._state[pulse.source] = pulse.pulse
        pulse_to_send = Pulse.low if all(p == Pulse.high for p in self._state.values()) else Pulse.high
        return self._dispatch(pulse_to_send)


class BroadcasterNode(Node):
    def apply(self, pulse: DirectedPulse) -> list[DirectedPulse]:
        return self._dispatch(pulse.pulse)


class ReceiverNode(Node):
    def apply(self, pulse: DirectedPulse) -> list[DirectedPulse]:
        return []


def build_network(input_lines: list[str]) -> dict[str, Node]:
    nodes = {}

    for line in input_lines:
        node, targets = line.split(" -> ")
        node_type = None
        if node == "broadcaster":
            node_type = BroadcasterNode
        elif node.startswith("%"):
            node = node.lstrip("%")
            node_type = FlipFlopNode
        elif node.startswith("&"):
            node = node.lstrip("&")
            node_type = ConjunctionNode
        else:
            node_type = ReceiverNode
        if node not in nodes:
            nodes[node] = {"node_type": None, "input_nodes": [], "output_nodes": []}
        nodes[node]["node_type"] = node_type
        nodes[node]["output_nodes"] = targets.split(", ")
        for output_node in nodes[node]["output_nodes"]:
            if output_node not in nodes:
                nodes[output_node] = {"node_type": ReceiverNode, "input_nodes": [], "output_nodes": []}
            nodes[output_node]["input_nodes"].append(node)

    return {key: node["node_type"](key, node["input_nodes"], node["output_nodes"]) for key, node in nodes.items()}  # type: ignore


def simulate(network: dict[str, Node]):
    next_pulses: list[DirectedPulse] = []
    pulses: list[DirectedPulse] = [DirectedPulse("broadcaster", Pulse.low, "button")]
    low_pulse_count = 0
    high_pulse_count = 0
    while pulses:
        low_pulse_count += sum(1 for p in pulses if p.pulse == Pulse.low)
        high_pulse_count += sum(1 for p in pulses if p.pulse == Pulse.high)
        for pulse in pulses:
            next_pulses.extend(network[pulse.destination].apply(pulse))
        pulses = list(next_pulses)
        next_pulses = []

    return low_pulse_count, high_pulse_count


def solve(input_lines: list[str]):
    network = build_network(input_lines)

    low_pulse_count = 0
    high_pulse_count = 0
    for _ in range(1000):
        low, high = simulate(network)
        low_pulse_count += low
        high_pulse_count += high

    return low_pulse_count * high_pulse_count


def main():
    with open("20/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
