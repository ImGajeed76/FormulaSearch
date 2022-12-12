from searcher import *

white = '\033[0m'  # white (normal)
red = '\033[31m'  # red
green = '\033[32m'  # green
orange = '\033[33m'  # orange
blue = '\033[34m'  # blue
purple = '\033[35m'  # purple
gray = '\033[90m'  # gray


def load_formulas(file_path: str):
    if not file_path.endswith(".fs"):
        return []

    formulas = []
    in_comment = False
    with open(f"{file_path}", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or line == "\n":
                continue
            if line.startswith('"""'):
                in_comment = not in_comment

            if not in_comment:
                formulas.append(Formula(*line.split("=")))
    return formulas


def console_app(formula_file: str):
    formulas = load_formulas(formula_file)
    searcher = FormulaSearcher(formulas)
    while True:
        print("\n" * 100)
        searched = input("Variable that is searched: ")
        if searched == "":
            continue
        to_use = input(f"Variables that you have access to {orange}(seperated with a , or leave empty){white}: ") \
            .replace(" ", "")
        if to_use == ",":
            continue

        if "," in to_use:
            to_use = to_use.removesuffix(",")
            to_use = to_use.split(",")

        try:
            results = searcher.deep_search(searched, to_use)
        except Exception as e:
            print(f"{red}Error: (probably no solution found)\n > {e}{white}")
            input(f"{gray}Press enter to continue...{white}")
            continue

        if len(results) == 0:
            print(f"{red}No solution found{white}")
            input(f"{gray}Press enter to continue...{white}")
            continue

        print()
        print("------------------------------------------")
        i = 1
        for result in results:
            print(f"Formula {orange}{i}{white}: {red}{result}{white}")
            i += 1
        print("------------------------------------------")
        print()

        if input(f"Would you like to insert values? (y/{green}N{white}) ") == "y":
            if len(results) > 1:
                index = int(input(f"Which formula should be used ({orange}1..{len(results)}{white}): ")) - 1
            else:
                index = 0
            values = {}
            for var in results[index].get_args(results[index].primary_variable):
                values.update({var: float(input(f"{var} = "))})
            formatted = "{:.3e}".format(float(str(results[index].run_with_values(values))))
            print(f"{red}p = {formatted}{white}")
            input(f"{gray}Press enter to continue...{white}")


if __name__ == '__main__':
    console_app("formulas.fs")
