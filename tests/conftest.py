"""Pytest fixtures."""

import pytest

from qspreadsheet import qt


@pytest.fixture(scope='session')
def qapp():
    """Yields instance of QApplication."""
    app = qt.QApplication([])
    yield app.instance()
    del app
