import sympy


class Line:
    def __init__(self, line: str):
        p, v = line.split(" @ ")
        self.x, self.y, self.z = map(int, p.split(", "))
        self.vx, self.vy, self.vz = map(int, v.split(", "))

    def __repr__(self):
        return f"Line({self.x}, {self.y}, {self.z} @ {self.vx}, {self.vy}, {self.vz})"
    
    @property
    def pos(self):
        return self.x, self.y, self.z
    
    @property
    def vel(self):
        return self.vx, self.vy, self.vz


def solve(input_lines: list[str]):
    lines = list(map(Line, input_lines))

    sx, sy, sz = sympy.var("sx"), sympy.var("sy"), sympy.var("sz")

    vx, vy, vz = sympy.var("vx"), sympy.var("vy"), sympy.var("vz")

    eq = []

    for i, line in enumerate(lines[:3]):
        ti = sympy.var("t{}".format(i))

        eq.append(sympy.Eq(sx + vx * ti, line.x + line.vx * ti))
        eq.append(sympy.Eq(sy + vy * ti, line.y + line.vy * ti))
        eq.append(sympy.Eq(sz + vz * ti, line.z + line.vz * ti))

    ans = sympy.solve(eq)[0]
    return ans[sx] + ans[sy] + ans[sz]


def main():
    with open("24/input.txt") as f:
        test_input = list(map(lambda line: line.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
