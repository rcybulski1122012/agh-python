from string import ascii_lowercase
from typing import Generator
from typing import Union

OPERATORS = "&|>"


def check(expr: str) -> int:
    brackets_counter = 0
    # "test"

    # status is equal to False if we expect a variable or "("
    # status is equal to True if we expect an operator of ")"
    status = False

    for char in expr:
        if status:
            if char not in OPERATORS + ")":
                return False
            elif char == ")":
                brackets_counter -= 1
            elif char in OPERATORS:
                status = False
        else:
            if char in OPERATORS + ")":
                return False
            elif char == "(":
                brackets_counter += 1
            elif char in ascii_lowercase:
                status = True

        if brackets_counter < 0:
            return False

    return brackets_counter == 0 and status


def bracket(expr: str) -> str:
    """Assumes that the given expression in valid"""
    while expr[0] == "(" and expr[-1] == ")" and check(expr[1:-1]):
        expr = expr[1:-1]

    return expr


def bal(expr: str, operators: list[str]) -> Union[int, None]:
    """Goes through the expression from right to left checking
    whether the current char is one of the given operators and is not inside any bracket, returning an index.
    If not found, it returns None

    Assumes that the given expression is valid and does not contain brackets at the beginning and end.
    """
    brackets_counter = 0

    for i, char in reversed(list(enumerate(expr))):
        if char == ")":
            brackets_counter += 1
        elif char == "(":
            brackets_counter -= 1
        elif char in operators and brackets_counter == 0:
            return i

    return None


def rnp(expr: str) -> str:
    """Transforms the given expression from algebraic form into RNP(Reversed Polish Notation)

    Assumes that the given expression is valid
    """
    expr = bracket(expr)

    if len(expr) == 1:
        return expr

    for operators in (list(">"), list("&|")):
        index = bal(expr, operators)

        if index is None:
            continue

        left = rnp(expr[:index])
        right = rnp(expr[index + 1 :])
        operator = expr[index]

        return f"{left}{right}{operator}"

    return ""


def map_values(expr: str, values: str) -> str:
    """Replaces variables in the expression with values.
    Values are matched by indexes in a way where the smallest alphabetically variable is matched
    to the first value and so on

    Assumes the length of values is equal to number of unique variables in the expression.
    """
    expr_list = list(expr)

    unique_vars = sorted(list({char for char in expr if char.isalpha()}))

    values_by_chars = dict(zip(unique_vars, values))

    for i, char in enumerate(expr_list):
        if char.isalpha():
            expr_list[i] = values_by_chars[char]

    return "".join(expr_list)


def gen(n: int) -> Generator[str, None, None]:
    for i in range(2**n):
        yield bin(i)[2:].rjust(n, "0")


def val(expr: str) -> str:
    """Evaluates the value of the RPN expression

    Assumes that the expression in valid.
    """
    stack: list[str] = []

    for char in expr:
        if char in OPERATORS:
            right, left = stack.pop(), stack.pop()

            if char == "&":
                evaluated = _bool_to_bin(right == left == "1")
            elif char == "|":
                evaluated = _bool_to_bin(right == "1" or left == "1")
            else:
                evaluated = _bool_to_bin(left == "0" or right == "1")

            stack.append(evaluated)
        else:
            stack.append(char)

    return stack[0]


def _bool_to_bin(value: bool) -> str:
    return "1" if value else "0"


def tautology(expr: str) -> bool:
    n = len({char for char in expr if char.isalpha()})

    for values in gen(n):
        mapped = map_values(expr, values)
        if val(mapped) == "0":
            return False

    return True
