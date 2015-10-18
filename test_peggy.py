import unittest
from peggy import memoize_


class TestPeggy(unittest.TestCase):
    def test_memoize_member_function(self):
        class SomeClass(object):
            def __init__(self):
                self._arr = []

            @memoize_
            def member(self, a_, b_):
                self._arr.append(a_)
                self._arr.append(b_)
                return [a_, b_]

        t = SomeClass()
        a = "Value a"
        b = "Value b"
        c = "Value c"
        self.assertIs(t.member(a, b), t.member(a, b))
        self.assertIsNot(t.member(a, b), t.member(a, c))
        self.assertIs(t.member(a, c), t.member(a, c))
