"""Table view."""

from typing import Optional

from qspreadsheet import qt


class TableView(qt.QTableView):
    """Table view."""

    def __init__(self, parent: Optional[qt.QObject] = ...) -> None:
        """Create TableView object.

        Args:
            parent: A QWidget, optional, to be assigned as parent.
        """
        super().__init__(parent)

    def contextMenuEvent(self, event: qt.QContextMenuEvent) -> None:
        """Handles right-clicking on a cell.

        When subclassing, you probably want to overrite
        `make_cell_context_menu`, not this function.

        Args:
            event: QContextMenuEvent to handle.
        """
        row_ndx = self.rowAt(event.y())
        col_ndx = self.columnAt(event.x())
        if row_ndx < 0 or col_ndx < 0:
            return

        menu = self.create_cell_context_menu(row_ndx, col_ndx)
        pos = self.mapToGlobal(event.pos())
        menu_pos = qt.QPoint(pos.x() + 20, pos.y() + menu.height() + 20)
        menu.exec_(menu_pos)

    def create_cell_context_menu(self, row_ndx: int, col_ndx: int) -> qt.QMenu:
        """Create cell context menu.

        Args:
            row_ndx: An int.
            col_ndx: An int.

        Returns:
            A QMenu.
        """
        menu = qt.QMenu('context menu', self)
        return menu
