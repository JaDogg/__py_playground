import unittest

from peggy.peggy import *
from peggy.display import *


class InfixTree(PackratParser):
    def __init__(self, text):
        rules = {
            "parse": [
                ["_", "exp0", Nothing(), label("parse")]
            ],
            "exp0": [
                ["exp1", ZeroOrMore(
                    Or(
                        One(r"([+])", "_", "exp1", label("exp0_add")),
                        One(r"([-])", "_", "exp1", label("exp0_sub"))
                    )
                ), label("exp0")]
            ],
            "exp1": [
                ["exp2", ZeroOrMore(
                    Or(
                        One(r"([*])", "_", "exp2", label("exp0_mul")),
                        One(r"([/])", "_", "exp2", label("exp0_div"))
                    )
                ), label("exp1")]
            ],
            "exp2": [
                ["exp3", ZeroOrOne(r"([\^])", "_", "exp2", label("exp0_pow")),
                 label("exp2")]
            ],
            "exp3": [
                [r"[\(]", "_", "exp0", r"[\)]", "_", label("exp3_paren")],
                [r"([-+])", "_", "exp1", label("exp3_neg")],
                [r"(\d+)", "_", label("exp3_int")]
            ],
            "_": [
                [r"\s*"]
            ]
        }
        PackratParser.__init__(self, rules, text)

    def parse(self):
        return self.parse_rule("parse")


class TestCalculator(unittest.TestCase):
    def test_calculator(self):
        t = r"""5+2*3+4"""
        p = InfixTree(t)
        _, _, t_ = p.parse()
        # t_, = t_
        print(build_dot(t_))
