from __future__ import absolute_import
import unittest

from peggy.peggy import *


class InfixTree(PackratParser):
    def __init__(self, text):
        rules = {
            "parse": [
                ["_", "exp0", Not(".")]
            ],
            "exp0": [
                ["exp1", ZeroOrMore(
                    Or(
                        One(r"([+])", "_", "exp1", "@do_math"),
                        One(r"([-])", "_", "exp1", "@do_math")
                    )
                )]
            ],
            "exp1": [
                ["exp2", ZeroOrMore(
                    Or(
                        One(r"([*])", "_", "exp2", "@do_math"),
                        One(r"([/])", "_", "exp2", "@do_math")
                    )
                )]
            ],
            "exp2": [
                ["exp3", Optional(r"([\^])", "_", "exp2", "@do_math")]
            ],
            "exp3": [
                [r"[\(]", "_", "exp0", r"[\)]", "_"],
                [r"([\-])", "_", "exp1", "@do_math"],
                [r"(\d+)", "_", "@to_int"]
            ],
            "_": [
                [r"\s*"]
            ]
        }
        PackratParser.__init__(self, rules, text)

    def do_math(self, *args):
        return args,

    def parse(self):
        return self.parse_rule("parse")


class Calculator(InfixTree):
    def __init__(self, text):
        InfixTree.__init__(self, text)

    def do_math(self, *args):

        lhs = None
        try:
            lhs, opr, rhs = args
        except ValueError:
            opr, rhs = args

        if lhs is None and opr == "-":
            return -rhs,
        elif lhs is None and opr == "+":
            return rhs,
        elif opr == "-":
            return lhs - rhs,
        elif opr == "+":
            return lhs + rhs,
        elif opr == "*":
            return lhs * rhs,
        elif opr == "/":
            return lhs / rhs,
        elif opr == "^":
            return lhs ** rhs,


class InfixToPostfixCompiler(InfixTree):
    def __init__(self, text):
        InfixTree.__init__(self, text)

    def do_math(self, *args):
        lhs = None
        try:
            lhs, opr, rhs = args
        except ValueError:
            opr, rhs = args

        print args
        if lhs is None and opr == "-":
            return (rhs, "neg"),
        elif lhs is None and opr == "+":
            return (rhs,),
        else:
            return (rhs, lhs, opr),

    def parse(self):
        _, _, tree = InfixTree.parse(self)
        return " ".join(map(str, flatten(tree)))


class TestCalculator(unittest.TestCase):
    def test_calculator(self):
        t = r"""5+2+2-1*3"""
        p = Calculator(t)
        _, _, t_ = p.parse()
        t_, = t_
        print(t_)

    def test_random_sequences(self):
        import random
        for _ in range(200):
            opers = ["+", "-", "*", "/"]
            numbers = (random.randrange(-100, 100) for _ in range(
                random.randrange(20, 30)))
            numbers = map(str, numbers)
            prob = [numbers[0]]
            for number in numbers[1:]:
                prob.append(opers[random.randrange(0, 3)])
                prob.append(number)
            prob = "".join(prob)
            self.assertEqual(eval(prob), self.calc(prob))

    def calc(self, t):
        p = Calculator(t)
        _, _, t_ = p.parse()
        t_, = t_
        return t_
