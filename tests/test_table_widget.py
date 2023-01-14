"""Test for the TableWidget object."""

import pytest

from qspreadsheet import table_widget as tw
from qspreadsheet import qt
from tests import util


def test_create(qtbot):
    """TableView can be created."""
    util.test_create(tw.TableWidget, qtbot=qtbot)


@pytest.mark.parametrize('obj_name, obj_type', [
    ('table_view', qt.QTableView),
    ('table_model', qt.QAbstractItemModel),
    ('filter_model', qt.QSortFilterProxyModel),
    ('header_view', qt.QHeaderView),
])
def test_has_attr(qtbot, obj_name, obj_type):
    """Has table view attribute."""
    table_widget = tw.TableWidget()
    qtbot.addWidget(table_widget)

    attr_name = f'_{obj_name}'
    assert hasattr(table_widget, attr_name)
    obj: qt.QObject = getattr(table_widget, attr_name)
    assert isinstance(obj, obj_type)
    assert obj.parent() is table_widget
    assert obj.objectName() == obj_name


def test_setup_ui(qtbot):
    """Test TableWidget.setup_ui()."""
    table_widget = tw.TableWidget()
    qtbot.addWidget(table_widget)

    table_widget.setup_ui()
    assert table_widget.layout().objectName() == 'central_layout'
    table_view_layout = table_widget.findChild(qt.QLayout, 'table_view_layout')
    assert (table_view_layout is not None
            and isinstance(table_view_layout, qt.QLayout))
    table_view = table_widget.findChild(qt.QTableView, 'table_view')
    assert table_view is not None
