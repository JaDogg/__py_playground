import unittest
from peggy.peggy import *


class KeyValueParser(PackratParser):
    def __init__(self, text):
        rules = {
            "parse": [
                ["line", "parse"],
                ["line"],
                []
            ],
            "line": [
                ["spaces", "keyValue", "end_line"],
                ["spaces", "end_line"]
            ],
            "keyValue": [
                ["key", "separatorAndValue", "@create_pair"]
            ],
            "key": [
                [r"([^=]+)"]
            ],
            "separatorAndValue": [
                [r"([=])(.*)", "@create_value"]
            ],
            "spaces": [
                [r"\s*"]
            ],
            "end_line": [
                [r"\r?\n"]
            ]
        }
        PackratParser.__init__(self, rules, text)

    def parse(self):
        return dict(self.parse_text())

    @staticmethod
    def create_pair(key, value):
        return (key, value),

    @staticmethod
    def create_value(_, value):
        return value,


class TestKeyValue(unittest.TestCase):
    def test_key_value_parser(self):
        t = r"""
        Key 1=Value 1
        Key 2=Value 2
        Key 3=Value 3
        """
        p = KeyValueParser(t)
        self.assertEqual(
            {"Key 1": "Value 1", "Key 2": "Value 2", "Key 3": "Value 3"},
            p.parse())
