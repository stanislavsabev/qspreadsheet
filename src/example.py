import sys
from typing import cast

import pandas as pd

import qspreadsheet as qs
from qspreadsheet import qt
from qspreadsheet.types import DF


class MainWindow(qt.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        central_widget = qt.QWidget(self)
        central_layout = qt.QVBoxLayout(central_widget)
        central_widget.setLayout(central_layout)
        table_view = create_table_view()

        table_layout = qt.QHBoxLayout()
        table_layout.addWidget(table_view)
        table_view.setParent(table_layout)
        central_layout.addLayout(table_layout)

        self.setCentralWidget(central_widget)
        self.setWindowTitle('qspreadsheet')
        self.resize(800, 480)


def create_table_view() -> qt.QWidget:
    table_view = qt.QWidget()
    return table_view


def main():
    app = qt.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
