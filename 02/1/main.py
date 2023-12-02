import re

class Game:
    game_re = re.compile(r"^Game (?P<id>\d+): (?P<grabs>((((\d+)\s(\w+),?\s?)+);?\s?)+)$")
    grap_re = re.compile(r"((?:\d+\s\w+,?\s?)+);?")
    cubes_re = re.compile(r"(?P<count>\d+)\s(?P<colour>\w+),?")

    def __init__(self, line: str):
        assert (m := self.game_re.match(line))
        self.id = int(m.group("id"))
        grabs_part = m.group("grabs")
        grabs = self.grap_re.findall(grabs_part)
        self.grabs: list[dict[str, int]] = [
            (cubes := self.cubes_re.findall(g)) and {
                c[1]: int(c[0])
                for c in cubes
            }
            for g in grabs
        ]
    
    def max_by_colour(self):
        colours = set(c for g in self.grabs for c in g)
        return {
            colour: max(g.get(colour, 0) for g in self.grabs)
            for colour in colours
        }

def solve(input_lines: list[str]):
    limits = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    def get_id_if_valid(line: str):
        game = Game(line)
        maxes = game.max_by_colour()
        if any(k not in limits for k in maxes):
            return 0
        if any(limits[k] < v for k, v in maxes.items()):
            return 0
        return game.id

    return sum(map(get_id_if_valid, input_lines))
        


def main():
    with open("02/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
