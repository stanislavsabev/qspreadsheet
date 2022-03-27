"""Example for how to use the `qspreadsheet` package."""

import sys

from qspreadsheet import qt


class MainWindow(qt.QMainWindow):
    """Main GUI Window."""

    def __init__(self, parent: qt.QWidget=None):
        """Init MainWindow object."""
        super().__init__(parent)

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
    """Create table view."""
    table_view = qt.QWidget()
    return table_view


def main():
    """Entry point for this script."""
    app = qt.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
