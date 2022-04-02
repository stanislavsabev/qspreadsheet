"""Test for the TableView object."""

from qspreadsheet import table_view
from tests import util


def test_create(qapp):  # pylint: disable=unused-argument
    """TableView can be created."""
    util.test_create(table_view.TableView)
