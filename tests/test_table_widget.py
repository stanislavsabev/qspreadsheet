"""Test for the TableWidget object."""

import pytest
import mock

from qspreadsheet import table_widget as tw
from qspreadsheet import qt
from tests import util


@pytest.fixture(scope='function')
def widget_mock(qapp):
    """Mock fixture for TableWidget."""
    table_widget_mock = mock.MagicMock()
    return table_widget_mock


@pytest.mark.serial
@pytest.fixture(scope='function')
def table_widget(qapp):
    """TableWidget fixture."""
    return tw.TableWidget()


@pytest.mark.serial
def test_create(qapp):
    """TableView can be created."""
    util.test_create(tw.TableWidget)


@pytest.mark.serial
@pytest.mark.parametrize('obj_name, obj_type', [
    ('table_view', qt.QTableView),
    ('table_model', qt.QAbstractItemModel),
    ('filter_model', qt.QSortFilterProxyModel),
    ('header_view', qt.QHeaderView),
])
def test_has_attr(table_widget, obj_name, obj_type):
    """Has table view attribute."""
    attr_name = f'_{obj_name}'
    assert hasattr(table_widget, attr_name)
    obj: qt.QObject = getattr(table_widget, attr_name)
    assert isinstance(obj, obj_type)
    assert obj.parent() is table_widget
    assert obj.objectName() == obj_name


@pytest.mark.serial
def test_setup_ui(table_widget):
    """Test TableWidget.setup_ui()."""
    table_widget.setup_ui()
    assert table_widget.layout().objectName() == 'central_layout'
    table_view_layout = table_widget.findChild(qt.QLayout, 'table_view_layout')
    assert (table_view_layout is not None
            and isinstance(table_view_layout, qt.QLayout))
    table_view = table_widget.findChild(qt.QTableView, 'table_view')
    assert table_view is not None
