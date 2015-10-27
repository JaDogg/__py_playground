from __future__ import absolute_import

import os
from StringIO import StringIO

from peggy.peggy import Label

_HTML_TEMPLATE = r"""
<html>
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.4.11/d3.min.js"></script>
<script src="http://cpettitt.github.io/project/graphlib-dot/v0.4.10/graphlib-dot.min.js"></script>
<script src="http://cpettitt.github.io/project/dagre-d3/v0.1.5/dagre-d3.min.js"></script>

<script>
<!--
window.onload = function() {
  // Parse the DOT syntax into a graphlib object.
  var g = graphlibDot.parse(
##graph##
  )

  // Render the graphlib object using d3.
  var renderer = new dagreD3.Renderer();
  renderer.run(g, d3.select("svg g"));


  // Optional - resize the SVG element based on the contents.
  var svg = document.querySelector('#graphContainer');
  var bbox = svg.getBBox();
  svg.style.width = bbox.width + 40.0 + "px";
  svg.style.height = bbox.height + 40.0 + "px";
}
-->
</script>
<style>
<!--
svg {
  overflow: hidden;
}
.node rect {
  stroke: #333;
  stroke-width: 1.5px;
  fill: #fff;
}
.edgeLabel rect {
  fill: #fff;
}
.edgePath {
  stroke: #333;
  stroke-width: 1.5px;
  fill: none;
}
-->
</style>
</head>
<body>
  <script type='text/javascript'>
  </script>
  <svg id="graphContainer">
    <g/>
  </svg>
</body>

</html>
"""


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


def display_labeled(items):
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
        _display_labeled(items)


def _display_labeled(items, depth=1):
    for item in items:
        if isinstance(item, Label):
            print("{t}({i})".format(t="  " * depth, i=item.label))
            _display_labeled(item, depth + 1)
        else:
            print("{t}{i}".format(t="  " * depth, i=item))


def _qt_render_dot(dot_string):
    from PyQt4.QtGui import QApplication
    from PyQt4.QtWebKit import QWebView
    html = _HTML_TEMPLATE.replace("##graph##", repr(dot_string))
    app = QApplication([])
    view = QWebView()
    view.setHtml(html)
    view.setWindowTitle("Peggy Dot Renderer")
    view.show()
    app.exec_()
