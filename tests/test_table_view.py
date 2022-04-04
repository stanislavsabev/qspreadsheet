"""Test for the TableView object."""

import pytest
from qspreadsheet import table_view
from tests import util


@pytest.mark.serial
def test_create(qapp):
    """TableView can be created."""
    util.test_create(table_view.TableView)
