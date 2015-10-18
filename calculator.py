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
                ["exp3", ZeroOrOne(r"([\^])", "_", "exp2", "@do_math")]
            ],
            "exp3": [
                [r"[\(]", "_", "exp0", r"[\)]", "_"],
                [r"([-+])", "_", "exp1", "@do_math"],
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
        t = r"""5+2+3"""
        p = InfixTree(t)
        _, _, t = p.parse()
        display(t)
