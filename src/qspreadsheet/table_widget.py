"""A TableWidget to implement and manage table and index views and models."""

from typing import Optional

from qspreadsheet.types import DF
from qspreadsheet import qt
from qspreadsheet import index_view
from qspreadsheet import index_model
from qspreadsheet import table_view
from qspreadsheet import table_model


class TableWidget(qt.QWidget):
    """A TableWidget to implement and manage table and index views and models.
    Based on QWidget.
    Handle setting column delegates.
    """

    def __init__(self, data: DF, parent: Optional[qt.QObject] = None) -> None:
        """Create TableWidget object.

        Args:
            parent: A QWidget, optional, to be assigned as parent.
        """
        super(TableWidget, self).__init__(parent)
        self._data = data

        self._data_model = table_model.TableModel(data, self)
        self.table_view = table_view.TableView(self)
        self.table_view.setModel(self._data_model)        
        
        self._row_index_model = index_model.RowIndexModel(data.index, self)
        self.row_index_view = index_view.IndexView('rows', self)
        self.row_index_view.setModel(self._row_index_model)

        self._col_index_model = index_model.ColumnIndexModel(data.columns, self)
        self.col_index_vew = index_view.IndexView('columns', self)
        self.col_index_vew.setModel(self._col_index_model)

        self._name_managed()
        self._setup_ui()

    def _name_managed(self):
        """Name managed Qt objects."""
        for attr_name in [a for a in dir(self) if not a.startswith('__') and a.startswith('_')]:
            attr = getattr(self, attr_name)
            if isinstance(attr, qt.QObject):
                attr.setObjectName(attr.__class__.__name__)

    def _setup_ui(self):
        """Setup UI layout for this widget."""
        
        self.setWindowTitle('Qspreadsheet - v0.0.1')
        self.col_index_vew.horizontalHeader().setVisible(False)
        self.col_index_vew.verticalHeader().setVisible(False)

        self.row_index_view.horizontalHeader().setVisible(False)        
        self.row_index_view.verticalHeader().setVisible(False)

        self.table_view.horizontalHeader().setVisible(False)        
        self.table_view.verticalHeader().setVisible(False)
        self._setup_table_grid_layout()

    def _setup_table_grid_layout(self):
        corner = qt.QLabel('corner')

        v = qt.QVBoxLayout()
        h = qt.QVBoxLayout()
        v.addLayout(h)
        grid_layout = qt.QGridLayout()
        h.addLayout(grid_layout)

        grid_layout.setObjectName('grid_layout')
        grid_layout.addWidget(corner, 0, 0, qt.Qt.AlignTop | qt.Qt.AlignLeft)
        grid_layout.addWidget(self.col_index_vew, 0, 1)
        grid_layout.addWidget(self.row_index_view, 1, 0)
        grid_layout.addWidget(self.table_view, 1, 1)
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 100)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 100)
        # grid_layout.setRowStretch(0, 0),
        # grid_layout.setRowStretch(1, 2)
        # grid_layout.setColumnStretch(0, 0)
        # grid_layout.setColumnStretch(1, 1)

        # grid_layout.setSpacing(0)
        # grid_layout.setContentsMargins(qt.QMargins(2, 1, 2, 1))
        self.setLayout(v)