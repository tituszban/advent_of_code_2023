from dataclasses import dataclass
import enum
from abc import ABC, abstractmethod
from typing import Callable, Optional
import networkx as nx
import matplotlib.pyplot as plt
import math


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
        self.node = node
        self.input_nodes = input_nodes
        self.output_nodes = output_nodes

    @abstractmethod
    def apply(self, pulse: DirectedPulse) -> list[DirectedPulse]:
        raise NotImplementedError

    def _dispatch(self, pulse: Pulse) -> list[DirectedPulse]:
        return [DirectedPulse(node, pulse, self.node) for node in self.output_nodes]

    @abstractmethod
    def to_g_node(self) -> tuple[str, dict[str, str]]:
        raise NotImplementedError

    def to_g_edge(self) -> list[tuple[str, str]]:
        return [(self.node, node) for node in self.output_nodes]

    @abstractmethod
    def state(self) -> str:
        raise NotImplementedError


class FlipFlopNode(Node):
    def __init__(self, node: str, input_nodes: list[str], output_nodes: list[str]):
        super().__init__(node, input_nodes, output_nodes)
        self._state = Pulse.low

    def apply(self, pulse: DirectedPulse):
        if pulse.pulse == Pulse.high:
            return []
        self._state = ~self._state
        return self._dispatch(self._state)

    def to_g_node(self) -> tuple[str, dict[str, str]]:
        return self.node, {
            "label": f"{self.node} [{self._state.value}]",
            "color": "green" if self._state == Pulse.high else "cyan",
        }

    def state(self) -> str:
        return "0" if self._state == Pulse.low else "1"


class ConjunctionNode(Node):
    def __init__(self, node: str, input_nodes: list[str], output_nodes: list[str]):
        super().__init__(node, input_nodes, output_nodes)
        self._state = {node: Pulse.low for node in input_nodes}

    def apply(self, pulse: DirectedPulse) -> list[DirectedPulse]:
        assert pulse.source in self._state
        self._state[pulse.source] = pulse.pulse
        pulse_to_send = Pulse.low if all(p == Pulse.high for p in self._state.values()) else Pulse.high
        return self._dispatch(pulse_to_send)

    def to_g_node(self) -> tuple[str, dict[str, str]]:
        if len(self.input_nodes) == 1:
            return self.node, {"label": f"{self.node} [inv]", "color": "orange"}
        return self.node, {
            "label": f"{self.node} [{sum(p == Pulse.high for p in self._state.values())}/{len(self.input_nodes)}]",
            "color": "red",
        }

    def state(self) -> str:
        return str(sum(p == Pulse.high for p in self._state.values()))


class BroadcasterNode(Node):
    def apply(self, pulse: DirectedPulse) -> list[DirectedPulse]:
        return self._dispatch(pulse.pulse)

    def to_g_node(self) -> tuple[str, dict[str, str]]:
        return self.node, {"label": self.node, "color": "blue"}

    def state(self) -> str:
        return "b"


class ReceiverNode(Node):
    def apply(self, pulse: DirectedPulse) -> list[DirectedPulse]:
        return []

    def to_g_node(self) -> tuple[str, dict[str, str]]:
        return self.node, {"label": self.node, "color": "yellow"}

    def state(self) -> str:
        return "r"


class SpyConjunctionNode(ConjunctionNode):
    def __init__(self, node: str, input_nodes: list[str], output_nodes: list[str], spy: Callable[[str], None]):
        super().__init__(node, input_nodes, output_nodes)
        self._spy = spy

    @classmethod
    def from_node(cls, node: ConjunctionNode, spy: Callable[[str], None]):
        return cls(node.node, node.input_nodes, node.output_nodes, spy)

    def apply(self, pulse: DirectedPulse) -> list[DirectedPulse]:
        result = super().apply(pulse)
        if any(h := [k for k, p in self._state.items() if p == Pulse.high]) > 0:
            self._spy(h[0])
        return result


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
    while pulses:
        for pulse in pulses:
            next_pulses.extend(network[pulse.destination].apply(pulse))
        pulses = list(next_pulses)
        next_pulses = []


def draw_network(network: dict[str, Node], leaf_count: int = 4):
    G = nx.DiGraph()
    next_nodes = ["broadcaster"]
    seen_nodes = set()
    while next_nodes:
        current_node = next_nodes.pop()
        node = network[current_node]

        G.add_node(current_node, **node.to_g_node()[1])

        for i, edge in enumerate(node.output_nodes):
            G.add_edge(current_node, edge)
            if edge in seen_nodes:
                continue
            seen_nodes.add(edge)
            next_nodes.append(edge)
            # Only display one leaf
            if current_node == "broadcaster" and i + 1 >= leaf_count:
                break

    pos = nx.spring_layout(G, k=0.1)
    plt.cla()
    nx.draw(
        G,
        pos,
        with_labels=True,
        labels={n: G.nodes[n]["label"] for n in G},
        node_color=[G.nodes[n]["color"] for n in G],
        font_weight="bold",
    )
    plt.show()


class Spy:
    def __init__(self, nodes: list[str]):
        self._min_seen: dict[str, Optional[int]] = {node: None for node in nodes}
        self._sim_step = 0

    def report_sim(self, i: int):
        self._sim_step = i

    def __call__(self, node: str) -> None:
        if self._min_seen[node] is None:
            self._min_seen[node] = self._sim_step + 1

    def get_solution(self):
        if all(self._min_seen.values()):
            return math.lcm(*self._min_seen.values())  # type: ignore


def solve(input_lines: list[str]):
    network = build_network(input_lines)

    goal = network["rx"]
    assert len(goal.input_nodes) == 1
    spy_node = goal.input_nodes[0]
    assert isinstance(network[spy_node], ConjunctionNode)
    spy = Spy(network[spy_node].input_nodes)
    network[spy_node] = SpyConjunctionNode.from_node(network[spy_node], spy)  # type: ignore

    for i in range(100000):
        spy.report_sim(i)
        simulate(network)
        if (solution := spy.get_solution()) is not None:
            return solution

        if i == 3965:
            draw_network(network, leaf_count=1)

    return 0


def main():
    with open("20/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
