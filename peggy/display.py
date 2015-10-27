from __future__ import absolute_import

import os
from StringIO import StringIO

from peggy.peggy import Label


def display(items, depth=1):
    for item in items:
        if isinstance(item, tuple):
            display(item, depth + 1)
        else:
            print("{t}({i})".format(t="  " * depth, i=item))


class _LabelToDotConverter(object):
    def __init__(self, items):
        self._items = items
        self._label_count = 0
        self._terminal_count = 0
        self._indent = 0
        self._dot = StringIO()

    def build_dot(self):
        self._write("digraph peggy_graph {")
        self._indent = 1
        self._build_dot(self._items, None)
        self._indent = 0
        self._write("}")

    def _build_dot(self, items, parent):
        for item in items:
            if isinstance(item, Label):
                self._label_count += 1
                label = "t" + str(self._label_count)
                self._write(label, " [shape=box,label=", '"',
                            item.label, '"];')
                if parent is not None:
                    self._write(parent, " -> ", label, ";")

                self._build_dot(item, label)
            else:
                self._terminal_count += 1
                label = "nt" + str(self._terminal_count)
                self._write(label, " [label=", '"',
                            str(item).encode("string_escape"), '"];')
                if parent is not None:
                    self._write(parent, " -> ", label, ";")

    def _write(self, *elements):
        self._dot.write("  " * self._indent)
        for element in elements:
            self._dot.write(str(element))
        self._dot.write(os.linesep)

    def get_dot(self):
        return self._dot.getvalue()


def build_dot(items):
    converter = _LabelToDotConverter(items)
    converter.build_dot()
    return converter.get_dot()
