"""Index model based on QAbstractTableModel."""

from typing import Any, Optional

import pandas as pd

from qspreadsheet.types import DF, SER
from qspreadsheet import logging
from qspreadsheet import qt
from qspreadsheet import resources_rc

logger = logging.getLogger(__name__)


class IndexModel(qt.QAbstractTableModel):
    """Index model based on QAbstractTableModel.

    Args:
        parent (QObject): Optional parent for this index.
    """

    mutable_rows_enabled = qt.Signal(bool)
    virtual_rows_enabled = qt.Signal(bool)

    def __init__(self, data: pd.Index, parent: Optional[qt.QObject] = ...) -> None:
        """Create IndexModel based on QAbstractTableModel.

        Args:
            parent (QObject): Model's parent
        """
        super(IndexModel, self).__init__(parent)
        self._data = data


class ColumnIndexModel(IndexModel):
    """Column index model based on QAbstractTableModel.

    Args:
        parent (QObject): Optional parent for this index.
    """

    def __init__(self, index: pd.Index, parent: Optional[qt.QObject] = ...) -> None:
        """Create ColumnIndexModel based on QAbstractTableModel.

        Args:
            parent (QObject): Model's parent
        """
        super().__init__(index, parent)
    
    def data(self, index: qt.QModelIndex, role: int = qt.Qt.DisplayRole) -> Any:
        return index.column()
    
    def columnCount(self, parent: qt.QModelIndex) -> int:
        del parent # Unused
        return self._data.size

    def rowCount(self, parent: qt.QModelIndex) -> int:
        del parent # Unused
        return 1


class RowIndexModel(IndexModel):
    """Row index model based on QAbstractTableModel.

    Args:
        parent (QObject): Optional parent for this index.
    """

    def __init__(self, index: pd.Index, parent: Optional[qt.QObject] = ...) -> None:
        """Create RowIndexModel based on QAbstractTableModel.

        Args:
            parent (QObject): Model's parent
        """
        super().__init__(index, parent)

    def data(self, index: qt.QModelIndex, role: int = qt.Qt.DisplayRole) -> Any:
        return index.row()

    def columnCount(self, parent: qt.QModelIndex) -> int:
        del parent # Unused
        return 1

    def rowCount(self, parent: qt.QModelIndex) -> int:
        del parent # Unused
        return self._data.size