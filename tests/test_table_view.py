"""Test for the TableView object."""

from qspreadsheet import table_view as tv
from tests import util


def test_create(qtbot):
    """TableView can be created."""
    table_view = util.test_create(tv.TableView, qtbot=qtbot)
    qtbot.addWidget(table_view)
