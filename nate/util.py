import StringIO
import os
import sys


class GrabStdOut(object):
    def __init__(self):
        self._real = sys.stdout
        self._str = StringIO.StringIO()

    def __enter__(self):
        sys.stdout = self._str
        return self

    def __exit__(self, type, value, traceback):
        sys.stdout = self._real

    @property
    def text(self):
        return self._str.getvalue()


def get_data_file(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "data", filename)


def read_data(filename):
    with open(get_data_file(filename), "r") as handle:
        return handle.read()


PY3 = sys.version_info[0] == 3

if PY3:
    STRING_TYPES = str,
else:
    STRING_TYPES = basestring,


def is_str(elem):
    return isinstance(elem, STRING_TYPES)
