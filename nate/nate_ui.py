from __future__ import absolute_import

import sys

from PyQt4 import QtGui
from nate import norvig


class NateUi(QtGui.QWidget):
    def __init__(self):
        super(NateUi, self).__init__()

        self.input_label = QtGui.QLabel('Input')
        self.output_label = QtGui.QLabel('Output')
        self.input_edit = QtGui.QTextEdit()
        self.output_edit = QtGui.QTextEdit()
        self.ok = QtGui.QPushButton("Ok")

        self.init()

    def init(self):
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.input_label, 1, 0)
        grid.addWidget(self.input_edit, 1, 1, 5, 1)

        grid.addWidget(self.output_label, 6, 0)
        grid.addWidget(self.output_edit, 6, 1, 5, 1)

        grid.addWidget(self.ok, 12, 0)
        self.ok.clicked.connect(self.process)

        self.setLayout(grid)

        self.setWindowTitle('Nate')
        self.show()

    def process(self):
        n = norvig.Norvig()
        self.output_edit.setText(n.process(self.input_edit.toPlainText()))


def main():
    app = QtGui.QApplication(sys.argv)
    ex = NateUi()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
