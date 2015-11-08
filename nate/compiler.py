from __future__ import absolute_import

import unittest
import sys

from pattern.search import compile as compile_pattern
from nate.util import read_data
from nate.vm import *
from peggy.peggy import *
from peggy.display import *

INSTRUCTIONS = {
    "fetch": Fetch,
    "push": Push,
    "call": CallFunc
}


class _CodeBuilder(Invoker):
    def __init__(self, instruction):
        self.instruction = instruction

    def __call__(self, *values):
        return INSTRUCTIONS[self.instruction](*values),


def codify(instruction):
    return _CodeBuilder(instruction)


class NateParser(PackratParser):
    def __init__(self, text):
        rules = {
            "parse": [
                [OneOrMore("line"), Nothing()]
            ],
            "line": [
                [r"#.*", "end_line"],
                ["keyValue", "end_line"],
                ["end_line"]
            ],
            "keyValue": [
                ["key", "separatorAndValue", "@create_rule"]
            ],
            "key": [
                ["lit"]  # TODO Improve this section
            ],
            "separatorAndValue": [
                [r"\=\=\>\>", "elems_"]
            ],
            "call": [
                ["id", r"[\(]", "elems", r"[\)]", "@codify_call", "@hug"]
            ],
            "elems": [
                ["elem", ZeroOrMore(r",", "elem")]
            ],
            "elems_": [
                ["elem", ZeroOrMore("_", "elem")]
            ],
            "elem": [
                ["pos", codify("fetch")],
                ["lit", codify("push")],
                ["call"]
            ],
            "_": [
                [r"(?: |\t)*"]
            ],
            "id": [
                [r"([a-zA-Z_]\w*)"]
            ],
            "pos": [
                [r'(\d+)', "@to_int"]
            ],
            "lit": [
                [r'"((?:\\.|[^"\\])*)"', "@unescape"]
            ],
            "end_line": [
                [r"\r?\n"]
            ]
        }
        PackratParser.__init__(self, rules, text + '\n')

    @staticmethod
    def unescape(string):
        if sys.version[0] == "2":
            return string.decode("string_escape"),
        else:
            return string.decode("unicode_escape"),

    @staticmethod
    def codify_call(*args):
        return args[:0:-1] + (CallFunc(args[0]),)

    @staticmethod
    def create_rule(*args):
        return (compile_pattern(args[0]), tuple(flatten(args[1:]))),

    def parse(self):
        return self.try_parse()

    def match_regex(self, position, token, values):
        # Skip using the rule '_', WHY: ignoring whitespace makes it easier to write
        # The grammar
        subtext = self._text[position:]
        matched = re.match(self._rules["_"][0][0] + token, subtext)

        if matched:
            new_position = position + matched.end()
            return new_position, new_position, values + matched.groups()

        return position, None, ()


def get_nate_logic():
    text = read_data("nate.txt")
    return NateParser(text).parse()


class TestNateParser(unittest.TestCase):
    def test_basic(self):
        display(get_nate_logic())
