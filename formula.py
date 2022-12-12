import sympy


class Formula:
    def __init__(self, left_side, right_side, primary_variable=None):
        self.solutions = []
        self.formula = sympy.sympify(f"({left_side}) - ({right_side})")
        if primary_variable is None:
            self.primary_variable = sympy.sympify(left_side).free_symbols.pop()
        else:
            self.primary_variable = primary_variable

    def solve(self, variable=None):
        if variable is None:
            variable = self.primary_variable

        solutions = sympy.solve(self.formula, variable)

        self.primary_variable = variable
        self.solutions = solutions

        return self

    def run_with_values(self, values):
        return sympy.solve(self.formula.subs(values), self.primary_variable)[0]

    def get_args(self, value):
        return list(self.formula.free_symbols - {value})

    def insert_formula(self, formula, variable):
        f = self.formula.subs({variable: formula.solutions[0]})
        return sympy.solve(f)

    def __str__(self):
        self.solve()
        return f"{self.primary_variable} = {self.solutions[0]}"
