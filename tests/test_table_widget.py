"""Test for the TableWidget object."""

from qspreadsheet import table_widget
from tests import util


def test_create(qapp):  # pylint: disable=unused-argument
    """TableView can be created."""
    util.test_create(table_widget.TableWidget)


def test_has_table_view_attr():
    """Has table view attribute."""
    sut = table_widget.TableWidget()
    assert hasattr(sut, '_table_view')
