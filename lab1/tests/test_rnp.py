import pytest

from lab1.rpn import check, bracket, bal, rnp, map_values, gen, val, tautology


@pytest.mark.parametrize("expr, expected", [
    ("a", True),
    ("a>b", True),
    ("(a)", True),
    ("(((a)))", True),
    ("a>b>c&a", True),
    ("(a|(((a>b)>(c|d))>(a&b)>(b)|g))", True),
    ("a<b", False),
    ("aa", False),
    ("((a)", False),
    ("((a>b", False),
    ("(a>(b&c)", False),
    ("(a|(((a>b)>(c|d))(a&b)>(b)|g))", False),
    ("a>", False)
])
def test_check(expr, expected):
    assert check(expr) == expected


@pytest.mark.parametrize("expr, expected", [
    ("a", "a"),
    ("(a)", "a"),
    ("(((((a)))))", "a"),
    ("(a)>(b)>(c)", "(a)>(b)>(c)"),
    ("((a>b)&(c>d))", "(a>b)&(c>d)"),
])
def test_bracket(expr, expected):
    assert bracket(expr) == expected


@pytest.mark.parametrize("expr, operators, expected", [
    ("a>(b>c)", list(">"), 1),
    ("a|b&c", list("&"), 3),
    ("a|(b&c)", list("&"), None),
    ("a|(b&c)", list("&|"), 1),
])
def test_bal(expr, operators, expected):
    assert bal(expr, operators) == expected


@pytest.mark.parametrize("expr, expected", [
    ("a&b", "ab&"),
    ("a>b>c", "ab>c>"),
    ("(a>(b|c))", "abc|>"),
])
def test_rnp(expr, expected):
    assert rnp(expr) == expected


@pytest.mark.parametrize("expr, values, expected", [
    ("ab&c|", "101", "10&1|"),
    ("ac>b>", "101", "11>0>")
])
def test_map_values(expr, values, expected):
    assert map_values(expr, values) == expected


def test_gen():
    n = 3
    expected = [
        "000", "001", "010", "011",
        "100", "101", "110", "111",
    ]

    assert list(gen(n)) == expected


@pytest.mark.parametrize("expr, expected", [
    ("10>", "0"),
    ("101>&", "1")
])
def test_val(expr, expected):
    assert val(expr) == expected


@pytest.mark.parametrize("expr, expected", [
    ("a", False),
    ("aa|", False),
    ("ab|c|", False),
    (rnp("(((a&b)>c)>(a>(b>c)))&((a>(b>c))>((a&b)>c))"), True),
])
def test_tautology(expr, expected):
    assert tautology(expr) == expected
