"""Example for how to use the `qspreadsheet` package."""

import sys
from typing import Callable, Optional

import pandas as pd

from qspreadsheet import qt
from qspreadsheet import table_widget


class MainWindow(qt.QMainWindow):
    """Main GUI Window."""

    def __init__(self, parent: Optional[qt.QWidget] = None):
        """Create MainWindow object.

        Args:
            parent (qt.QWidget, optional): Window's parent. Defaults to None.
        """
        super(MainWindow, self).__init__(parent)
        self._window_settings = qt.QSettings(qt.QSettings.IniFormat,
                                qt.QSettings.UserScope,
                                'qt',
                                'qspreadsheet')
        self._settings_group = self.__class__.__name__
        self._default_size = qt.QSize(800, 480)
        central_widget = qt.QWidget(self)
        central_layout = qt.QVBoxLayout(central_widget)
        central_widget.setLayout(central_layout)
        
        self.setCentralWidget(central_widget)
        self.setWindowTitle('qspreadsheet')
        self.load_settings()

    def closeEvent(self, event: qt.QCloseEvent):
        """Handles the close event for this window

        Args:
            event (qt.QCloseEvent): close event.
        """
        self.save_settings()
        event.accept()

    def save_settings(self):
        """Save window settings like size and position.

        Args:
            settings (qt.QSettings): Window settings.
        """
        settings = self._window_settings
        settings.beginGroup(self._settings_group)
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())
        settings.endGroup()

    def load_settings(self):
        """Load window settings like size and position.

        Args:
            settings (qt.QSettings): Window settings.
        """
        settings = self._window_settings
        settings.beginGroup(self._settings_group)
        self.resize(qt.QSize(settings.value('size', self._default_size)))  # type: ignore
        self.move(qt.QPoint(settings.value('pos', qt.QPoint(200, 200))))  # type: ignore
        settings.endGroup()

    def add_table(self, tbl_widget: qt.QWidget):
        central_layout = self.centralWidget().layout()
        tbl_layout = qt.QHBoxLayout()
        tbl_layout.addWidget(tbl_widget)
        tbl_widget.setParent(tbl_layout)
        central_layout.addLayout(tbl_layout)


def load_df():
    area = pd.Series({0 : 423967, 1: 695662, 2: 141297, 3: 170312, 4: 149995})
    pop = pd.Series({0 : 38332521, 1: 26448193, 2: 19651127, 3: 19552860, 4: 12882135})
    states = ['California', 'Texas', 'New York', 'Florida', 'Illinois']
    data = {'states': states, 'area': area, 'pop': pop}
    df = pd.DataFrame(data=data)
    df['overcrowded'] = (df['pop'] / df['area'] > 100)
    return df


def main():
    """Entry point for this script."""
    app = qt.QApplication(sys.argv)
    tbl_widget = table_widget.TableWidget(data=load_df())
    window = MainWindow()
    window.add_table(tbl_widget)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
