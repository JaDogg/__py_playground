from __future__ import absolute_import

import os
from StringIO import StringIO
from tempfile import NamedTemporaryFile
import webbrowser

from peggy.peggy import Label

_HTML_TEMPLATE_FILE = "data/dot_renderer.html"
_HTML_TEMPLATE = ""


def __init():
    global _HTML_TEMPLATE
    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, _HTML_TEMPLATE_FILE), "r") as html:
        _HTML_TEMPLATE = html.read()


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
                self._write(label, " [shape=box,label=", '"(',
                            item.label, ')"];')
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


def display(items, depth=1):
    for item in items:
        if isinstance(item, tuple):
            display(item, depth + 1)
        else:
            print("{t}({i})".format(t="  " * depth, i=item))


def display_labeled(items, depth=1):
    for item in items:
        if isinstance(item, Label):
            print("{t}({i})".format(t="  " * depth, i=item.label))
            display_labeled(item, depth + 1)
        else:
            print("{t}{i}".format(t="  " * depth, i=item))


def render_labeled(items):
    converter = _LabelToDotConverter(items)
    converter.build_dot()
    return _display_dot_string_in_browser(converter.get_dot())


def _display_dot_string_in_browser(dot_string):
    html = _HTML_TEMPLATE.replace("##graph##", repr(dot_string))
    f = NamedTemporaryFile(suffix="_peg.html", delete=False)
    f.write(html)
    webbrowser.open(f.name)


__init()
