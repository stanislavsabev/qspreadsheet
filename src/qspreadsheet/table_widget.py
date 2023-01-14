"""A TableWidget to implement and manage table and index views and models."""

from qspreadsheet import qt
from qspreadsheet import table_view
from qspreadsheet import table_model


class TableWidget(qt.QWidget):
    """A TableWidget to implement and manage table and index views and models.
    Based on QWidget.
    Handle setting column delegates.
    """

    def __init__(self, parent: qt.QWidget = None) -> None:
        """Create TableWidget object.

        Args:
            parent: A QWidget, optional, to be assigned as parent.
        """
        super().__init__(parent)
        self._table_view = table_view.TableView(self)
        self._table_model = table_model.TableModel(parent=self)
        self._filter_model = qt.QSortFilterProxyModel(self)
        self._header_view = qt.QHeaderView(qt.Qt.Horizontal, self)
        self.name_managed()
        self.setup_ui()

    def name_managed(self):
        """Name managed Qt objects."""
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
