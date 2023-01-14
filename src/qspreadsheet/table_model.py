"""Table model based on QAbstractTableModel."""

import typing as t 

from qspreadsheet import logging
from qspreadsheet import qt
from qspreadsheet import resources_rc

logger = logging.getLogger(__name__)


class TableModel(qt.QAbstractTableModel):
    """Table model based on QAbstractTableModel.

    Args:
        parent (QObject): Model's parent
    """

    mutable_rows_enabled = qt.Signal(bool)
    virtual_rows_enabled = qt.Signal(bool)

    def __init__(self, parent: t.Optional[qt.QObject] = ...) -> None:
        """Create TableModel based on QAbstractTableModel.

        Args:
            parent (QObject): Model's parent
        """
        super(TableModel, self).__init__(parent)
