"""Table widget."""

from qspreadsheet import qt
from qspreadsheet import table_view


class TableWidget(qt.QWidget):
    """Table widget."""

    def __init__(self, parent: qt.QWidget = None) -> None:
        """Create TableWidget object.

        Args:
            parent: A QWidget, optional, to be assigned as parent.
        """
        super().__init__(parent)

        self._table_view = table_view.TableView(self)

        table_view_layout = qt.QVBoxLayout()
        table_view_layout.setObjectName('table_view_layout')
        table_view_layout.addWidget(self._table_view)
        central_layout = qt.QVBoxLayout(self)
        central_layout.setObjectName('central_layout')
        central_layout.addLayout(table_view_layout)

        self.setLayout(central_layout)
        self.setWindowTitle('qspreadsheet')
