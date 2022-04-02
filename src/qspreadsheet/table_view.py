"""Table view."""

from qspreadsheet import qt


class TableView(qt.QTableView):
    """Table view."""

    def __init__(self, parent: qt.QWidget = None) -> None:
        """Create TableView object.

        Args:
            parent: A QWidget, optional, to be assigned as parent.
        """
        super().__init__(parent)
