from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebView

__author__ = 'bhathiyap'

template = r"""
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


# References:
# http://stackoverflow.com/a/13386109/1355145
# https://pythonspot.com/qt4-window/
# http://stackoverflow.com/a/20981629/1355145

def render_dot(dot_string):
    html = template.replace("##graph##", repr(dot_string))
    app = QApplication([])
    view = QWebView()
    view.setHtml(html)
    view.setWindowTitle("Peggy Dot Renderer")
    view.show()
    app.exec_()
