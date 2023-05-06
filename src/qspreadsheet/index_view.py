"""IndexView view."""

from typing import Optional, Union

from qspreadsheet import qt


class IndexView(qt.QTableView):
    """Table view."""

    def __init__(self, orientation: qt.Qt.Orientation, parent: Optional[qt.QObject] = None) -> None:
        """Create IndexView object.

        Args:
            parent: A QWidget, optional, to be assigned as parent.
        """
        super().__init__(parent)
        self.orientation = orientation
        self.table_view: qt.QTableView = parent.table_view
        self.setSizePolicy(qt.QSizePolicy(qt.QSizePolicy.Maximum, qt.QSizePolicy.Maximum))
        # Automatically stretch rows/columns as widget is resized
        if self.orientation == qt.Qt.Vertical:
            self.horizontalHeader().setSectionResizeMode(qt.QHeaderView.ResizeMode.Stretch)


    def count(self) -> int:
        x = 0
        if self.orientation == qt.Qt.Vertical:
            x = self.model().rowCount(qt.QModelIndex())
        else:
            x = self.model().columnCount(qt.QModelIndex())
        return x

    # def sizeHint(self) -> qt.QSize:
    #     """Return the size of the header needed to match the corresponding Table View

    #     Returns:
    #         qt.QSize: Size hint.
    #     """
    #     fm = qt.QFontMetrics(self.font())

    #     # Columm headers
    #     if self.orientation == qt.Qt.Horizontal:
    #         # Width of DataTableView
    #         width = self.table_view.sizeHint().width() + self.verticalHeader().width()
    #         # Height
    #         height = 2 * self.frameWidth()  # Account for border & padding
    #         for i in range(self.count()):
    #             height += self.rowHeight(i)

    #     # Index header
    #     else:
    #         # Height of DataTableView
    #         height = self.table_view.sizeHint().height() + self.horizontalHeader().height()
    #         # Width
    #         width = 2 * self.frameWidth()  # Account for border & padding
    #         for i in range(self.count()):
    #             width += max(self.columnWidth(i), 100)
    #     return qt.QSize(width, height)

    # This is needed because otherwise when the horizontal header is a single row it will add whitespace to be bigger
    def minimumSizeHint(self):
        if self.orientation == qt.Qt.Horizontal:
            return qt.QSize(0, self.sizeHint().height())
        else:
            return qt.QSize(self.sizeHint().width(), 0)


    def sizeHint(self):
        if self.orientation == qt.Qt.Horizontal:
            width = self.columnWidth(0)
            height = self.dataframe_viewer.columnHeader.sizeHint().height()
        else:  # Vertical
            width = self.dataframe_viewer.indexHeader.sizeHint().width()
            height = self.rowHeight(0) + 2

        return qt.QtCore.QSize(width, height)