import logging
from typing import List, Optional

from qspreadsheet import qt
from qspreadsheet.common import standard_icon
from qspreadsheet.custom_widgets import LabeledLineEdit
from qspreadsheet import resources_rc

logger = logging.getLogger(__name__)


class FilterWidgetAction(qt.QWidgetAction):
    """Checkboxes list filter menu"""

    all_deselected = qt.Signal(bool)

    def __init__(self, parent=None) -> None:
        """Checkbox list filter menu

        Arguments
        ----------

        parent: (Widget)
            Parent

        menu: (QMenu)
            Menu object this list is located on
        """
        super(FilterWidgetAction, self).__init__(parent)

        # Build Widgets
        widget = qt.QWidget()
        layout = qt.QVBoxLayout()

        self.str_filter = LabeledLineEdit("Filter", parent=parent)
        layout.addWidget(self.str_filter)

        self.list = qt.QListWidget(widget)
        self.list.setStyleSheet(
            """
            QListView::item:selected {
                background: rgb(195, 225, 250);
                color: rgb(0, 0, 0);
            } """
        )
        self.list.setMinimumHeight(150)
        self.list.setUniformItemSizes(True)

        layout.addWidget(self.list)

        # This button in made visible if the number
        # of items to show is more than the initial limit
        btn = qt.QPushButton("Not all items showing")

        btn.setIcon(standard_icon("MessageBoxWarning"))
        btn.setVisible(False)
        layout.addWidget(btn)
        self.show_all_btn = btn
        self.select_all_item: Optional[qt.QListWidgetItem] = None

        widget.setLayout(layout)
        self.setDefaultWidget(widget)

        # Signals/slots
        self.list.itemChanged.connect(self.on_listitem_changed)
        self.num_checked = 0

    def addItem(self, item: qt.QListWidgetItem):
        if item.checkState() == qt.Qt.Checked:
            self.num_checked += 1
        self.list.addItem(item)

    def addSelectAllItem(self, state: qt.Qt.CheckState) -> qt.QListWidgetItem:
        """Adding '(Select All)' item at the beginning of the QListWidget"""
        item = qt.QListWidgetItem("(Select All)")
        item.setFlags(item.flags() | qt.Qt.ItemIsUserCheckable)
        item.setCheckState(state)
        self.select_all_item = item
        self.list.insertItem(0, item)

        return item

    def clear(self):
        self.list.clear()
        self.num_checked = 0
        self.all_deselected.emit(True)

    @property
    def list_items_count(self) -> int:
        """Number of list items, excluding the '(Select All)' item"""
        return self.list.count() - 1

    def on_listitem_changed(self, item: qt.QListWidgetItem):
        self.list.blockSignals(True)
        if item is self.select_all_item:
            # Handle "select all" item click
            state = item.checkState()
            # Select/deselect all items
            for i in range(self.list.count()):
                itm = self.list.item(i)
                if itm is self.select_all_item:
                    continue
                itm.setCheckState(state)

            all_unchecked = state == qt.Qt.Unchecked
            # -1 is for the select_all_item
            self.num_checked = 0 if all_unchecked else self.list_items_count
        else:
            # Non "select all" item
            if item.checkState() == qt.Qt.Unchecked:
                self.num_checked -= 1
            elif item.checkState() == qt.Qt.Checked:
                self.num_checked += 1
            assert self.num_checked >= 0

            # figure out what "select all" should be
            state = (
                qt.Qt.Checked
                if self.num_checked == self.list_items_count
                else qt.Qt.Unchecked
            )
            # if state changed
            if state != self.select_all_item.checkState():
                self.select_all_item.setCheckState(state)

        if self.num_checked == 0:
            self.all_deselected.emit(True)
        else:
            self.all_deselected.emit(False)

        self.list.scrollToItem(item)
        self.list.blockSignals(False)

    def values(self) -> List[str]:
        checked = []
        for i in range(self.list.count()):
            itm = self.list.item(i)
            if itm is self.select_all_item:
                continue
            if itm.checkState() == qt.Qt.Checked:
                checked.append(itm.text())
        return checked
