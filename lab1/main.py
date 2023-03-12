from lab1.rpn import check
from lab1.rpn import rnp
from lab1.rpn import tautology

while True:
    expr = input("Podaj wyrażenie:")

    if expr == "q":
        break

    if not check(expr):
        print("ERROR")
        continue

    rnp_expr = rnp(expr)

    print("TAK" if tautology(rnp_expr) else "NIE")
