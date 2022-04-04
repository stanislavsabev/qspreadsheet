"""Pytest fixtures."""

import pytest

from qspreadsheet import qt


@pytest.fixture(scope='session')
def qapp():
    """Yields instance of QApplication."""
    app = qt.QApplication.instance()
    if app is None:
        app = qt.QApplication([])
    return app
