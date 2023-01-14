"""Example for how to use the `qspreadsheet` package."""

import sys
from typing import Callable, Optional

from qspreadsheet import qt
from qspreadsheet import table_widget


class MainWindow(qt.QMainWindow):
    """Main GUI Window."""

    def __init__(self, parent: Optional[qt.QWidget] = ...):
        """Create MainWindow object.

        Args:
            parent (qt.QWidget, optional): Window's parent. Defaults to None.
        """
        super(MainWindow, self).__init__(parent)

        self._org = 'qt'
        self._app = 'qspreadsheet'
        self._default_size = qt.QSize(800, 480)

        central_w = qt.QWidget(self)
        central_l = qt.QVBoxLayout(central_w)
        central_w.setLayout(central_l)
        table_w = table_widget.TableWidget()

        table_l = qt.QHBoxLayout()
        table_l.addWidget(table_w)
        table_w.setParent(table_l)
        central_l.addLayout(table_l)

        self.setCentralWidget(central_w)
        self.setWindowTitle('qspreadsheet')
        self.apply_settings(self.load_settings)

    def closeEvent(self, event: qt.QCloseEvent):
        """Handles the close event for this window

        Args:
            event (qt.QCloseEvent): close event.
        """
        self.apply_settings(self.save_settings)
        event.accept()

    def apply_settings(self, func: Callable[[qt.QSettings], None]):
        """Apply window settings ot own group and close it.

        Args:
            func (Callable[[qt.QSettings], None]): Settings function.
        """
        settings = qt.QSettings(qt.QSettings.IniFormat,
                                qt.QSettings.UserScope,
                                self._org,
                                self._app)
        settings.beginGroup('MainWindow')
        func(settings)
        settings.endGroup()

    def save_settings(self, settings: qt.QSettings):
        """Save window settings like size and position.

        Args:
            settings (qt.QSettings): Window settings.
        """
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())

    def load_settings(self, settings: qt.QSettings):
        """Load window settings like size and position.

        Args:
            settings (qt.QSettings): Window settings.
        """
        self.resize(qt.QSize(settings.value('size', self._default_size)))  # type: ignore
        self.move(qt.QPoint(settings.value('pos', qt.QPoint(200, 200))))  # type: ignore


def main():
    """Entry point for this script."""
    app = qt.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
