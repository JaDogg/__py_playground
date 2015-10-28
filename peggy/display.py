from __future__ import absolute_import

import os
from StringIO import StringIO

from peggy.peggy import Label

_HTML_TEMPLATE_FILE = "data/template.html"
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


def render_labeled(items):
    converter = _LabelToDotConverter(items)
    converter.build_dot()
    return _render_dot_or_print(converter.get_dot(), items)


# References:
# http://stackoverflow.com/a/13386109/1355145
# http://stackoverflow.com/a/20981629/1355145
# http://stackoverflow.com/a/24736418/1355145
# https://pythonspot.com/qt4-window/

def _render_dot_or_print(dot_string, items):
    try:
        _qt_render_dot(dot_string)
    except ImportError:
        display_labeled(items)


def display_labeled(items, depth=1):
    for item in items:
        if isinstance(item, Label):
            print("{t}({i})".format(t="  " * depth, i=item.label))
            display_labeled(item, depth + 1)
        else:
            print("{t}{i}".format(t="  " * depth, i=item))


def _qt_render_dot(dot_string):
    from PyQt4.QtGui import QApplication
    from PyQt4.QtWebKit import QWebView
    from PyQt4.QtNetwork import QNetworkProxyFactory
    html = _HTML_TEMPLATE.replace("##graph##", repr(dot_string))
    QNetworkProxyFactory.setUseSystemConfiguration(True)
    app = QApplication([])
    view = QWebView()
    view.setHtml(html)
    view.setWindowTitle("Peggy Dot Renderer")
    view.show()
    app.exec_()


__init()
