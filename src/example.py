"""Example for how to use the `qspreadsheet` package."""

import sys
from typing import Callable

from qspreadsheet import qt


class MainWindow(qt.QMainWindow):
    """Main GUI Window."""

    def __init__(self, parent: qt.QWidget=None):
        """Init MainWindow object."""
        super().__init__(parent)

        self._org = 'qt'
        self._app = 'qspreadsheet'
        self._default_size = qt.QSize(800, 480)

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
        self.apply_settings(self.load_settings)

    def closeEvent(self, event: qt.QCloseEvent): # pylint: disable=invalid-name
        """Pyside2-closeEvent."""
        self.apply_settings(self.save_settings)
        event.accept()

    def apply_settings(self, func: Callable[[qt.QSettings], None]):
        """Apply window settings ot own group and close it."""
        settings = qt.QSettings(qt.QSettings.IniFormat,
                                qt.QSettings.UserScope,
                                self._org,
                                self._app)
        settings.beginGroup('MainWindow')
        func(settings)
        settings.endGroup()

    def save_settings(self, settings: qt.QSettings):
        """Save window settings like size and position."""
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())

    def load_settings(self, settings: qt.QSettings):
        """Load window settings like size and position."""
        self.resize(qt.QSize(settings.value('size', self._default_size))) # type: ignore
        self.move(qt.QPoint(settings.value('pos', qt.QPoint(200, 200)))) # type: ignore

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
