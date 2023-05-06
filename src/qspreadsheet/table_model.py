"""Table model based on QAbstractTableModel."""

from typing import Any, Optional 

import pandas as pd

from qspreadsheet import logging
from qspreadsheet import qt
from qspreadsheet import resources_rc
from qspreadsheet.types import DF

logger = logging.getLogger(__name__)


class TableModel(qt.QAbstractTableModel):
    """Table model based on QAbstractTableModel.

    Args:
        parent (QObject): Optional parent for this model.
    """

    mutable_rows_enabled = qt.Signal(bool)
    virtual_rows_enabled = qt.Signal(bool)

    def __init__(self, data: DF, parent: Optional[qt.QObject] = None) -> None:
        """Create TableModel based on QAbstractTableModel.

        Args:
            parent (QObject): Model's parent
        """
        super(TableModel, self).__init__(parent)
        self._data = data

    def columnCount(self, parent: qt.QModelIndex) -> int:
        del parent # Unused
        return self._data.columns.size

    def rowCount(self, parent: qt.QModelIndex) -> int:
        del parent # Unused
        return self._data.index.size

    def data(self, index: qt.QModelIndex, role: int = qt.Qt.DisplayRole) -> Any:
        # logger.debug('data({}, {}), role: {}'.format( index.row(), index.column(), role))
        if index.row() < 0:
            logger.error('index.row() < 0')
            return None
        
        if role == qt.Qt.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        return None
