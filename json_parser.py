from __future__ import print_function

import json
import unittest
import sys

from peggy.peggy import PackratParser, Not, ZeroOrMore

# References : https://github.com/antlr/grammars-v4/blob/master/json/JSON.g4


class JsonParser(PackratParser):
    def __init__(self, text):
        rules = {
            "parse": [
                ["_", "object", "_", Not(r".")],
                ["_", "array", "_", Not(r".")],
            ],
            "object": [
                [r"[{]", "_", "pair", "_",
                 ZeroOrMore("_", r"[,]", "_", "pair"), "_", r"[}]", "@dict_"],
                [r"[{]", "_", r"[}]", "@empty_dict"]
            ],
            "array": [
                [r"[\[]", "_", "value", "_",
                 ZeroOrMore("_", r"[,]", "_", "value"), r"[\]]", "@list_"],
                [r"[\[]", "_", r"[\]]", "@empty_list"]
            ],
            "pair": [
                ["_", "string", "_", r"[:]", "_", "value", "_", "@hug"]
            ],
            "value": [
                ["string"],
                ["number"],
                ["object"],
                ["array"],
                [r"(true)", "@special"],
                [r"(false)", "@special"],
                [r"(null)", "@special"]
            ],
            "string": [
                [r'"((?:\\.|[^"\\])*)"', "@unescape"]
            ],
            "number": [
                [r"(\d+)", "@to_int"]
            ],
            "_": [
                [r"\s*"]
            ]
        }
        PackratParser.__init__(self, rules, text)

    def parse(self):
        return self.try_parse()

    @staticmethod
    def dict_(*args):
        return dict(args),

    @staticmethod
    def empty_dict(*_):
        return {},

    @staticmethod
    def list_(*args):
        return list(args),

    @staticmethod
    def empty_list(*_):
        return [],

    @staticmethod
    def unescape(string):
        if sys.version[0] == "2":
            return string.decode("string_escape"),
        else:
            return string.decode("unicode_escape"),

    @staticmethod
    def special(value):
        if value == "true":
            return True,
        elif value == "false":
            return False,
        elif value == "null":
            return None,

        assert False, "Invalid Special {val}".format(val=value)


class TestJsonParser(unittest.TestCase):
    def test_json_basic(self):
        objects = [
            {"he\\l\"lo": "world", "hi": {"alternative": "reality"}},
            {"null_checker": None, "hi": {"false": False, "true": True}},
            [["A"], "2", [[[]], []]],
            {"Hello": None, "World": [[[1]]]}
        ]
        for obj in objects:
            s = json.dumps(obj)
            parser = JsonParser(s)
            parsed_object, = parser.parse()
            print("Original::\n{obj}\nParsed::\n{parsed}\n\n".format(
                obj=s, parsed=json.dumps(parsed_object)))
            self.assertEqual(obj, parsed_object)
