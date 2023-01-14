"""Table widget."""

from qspreadsheet import qt
from qspreadsheet import table_view


class TableWidget(qt.QWidget):
    """Table widget.

    Manage:
        table_view, table_model, filter_model, header_view and header_model.
    Handle setting column delegates.
    """

    def __init__(self, parent: qt.QWidget = None) -> None:
        """Create TableWidget object.

        Args:
            parent: A QWidget, optional, to be assigned as parent.
        """
        super().__init__(parent)
        self._table_view = table_view.TableView(self)
        self._table_model = qt.QStandardItemModel(parent=self)
        self._filter_model = qt.QSortFilterProxyModel(self)
        self._header_view = qt.QHeaderView(qt.Qt.Horizontal, self)
        self.name_objects()
        self.setup_ui()

    def name_objects(self):
        """Name Qt objects."""
        for name in [
                'table_view', 'table_model', 'filter_model', 'header_view']:
            attr: qt.QObject = getattr(self, f'_{name}')
            attr.setObjectName(name)

    def setup_ui(self):
        """Setup UI layout for this widget."""
        table_view_layout = qt.QVBoxLayout()
        table_view_layout.setObjectName('table_view_layout')
        table_view_layout.addWidget(self._table_view)
        central_layout = qt.QVBoxLayout(self)
        central_layout.setObjectName('central_layout')
        central_layout.addLayout(table_view_layout)
        self.setLayout(central_layout)
        self.setWindowTitle('qspreadsheet')
