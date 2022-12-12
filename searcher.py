import sympy

from formula import Formula


def remove_duplicates(list_of_lists):
    return [list(x) for x in set(tuple(x) for x in list_of_lists)]


def remove_duplicate_formulas(formulas):
    fs = []
    out = []
    for formula in formulas:
        if str(formula) not in fs:
            fs.append(str(formula))
            out.append(formula)
    return out


def get_all_variables(formulas, variable, max_depth=10):
    if max_depth == 0:
        return []
    possible_variables = []
    for formula in formulas:
        if sympy.sympify(variable) in formula.formula.free_symbols:
            other = list(formula.formula.free_symbols - {sympy.sympify(variable)})
            possible_variables.append(other)
    return remove_duplicates(possible_variables)


class FormulaSearcher:
    def __init__(self, formulas):
        self.formulas = formulas

    def deep_search(self, searched: str | float, to_use=None, max_depth=10) -> list[Formula] | None:
        if to_use is None:
            to_use = []

        if type(searched) == str:
            searched = sympy.sympify(searched)

        to_use_temp = []
        for var in to_use:
            if type(var) == str:
                to_use_temp.append(sympy.sympify(var))
            else:
                to_use_temp.append(var)
        to_use = to_use_temp

        if max_depth == 0:
            return None

        solutions = self.search(searched)

        if len(to_use) == 0:
            return solutions

        for solution in solutions:
            args = solution.get_args(searched)
            no_others = True
            for var in args:
                if var not in to_use:
                    no_others = False
                    solution_for_arg = self.deep_search(var, to_use, max_depth - 1)
                    if solution_for_arg is not None:
                        solution_for_arg[0].solve(var)
                        s = solution.insert_formula(solution_for_arg[0], var)
                        if s:
                            key = list(s[0].keys())[0]
                            val = list(s[0].values())[0]
                            return [Formula(str(key), str(val), searched)]
            if no_others:
                return [solution]

        return solutions

    def search(self, variable) -> list[Formula]:
        solutions = []
        for formula in self.formulas:
            if variable in formula.formula.free_symbols:
                solutions.append(formula.solve(variable))
        return solutions
