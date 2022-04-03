"""Test package imports."""

import importlib
import pytest


def test_package_import():
    """Test package import."""
    result = True
    try:
        importlib.import_module('qspreadsheet')
    except ImportError:
        result = False
    finally:
        assert result


@pytest.mark.parametrize('module_name', [
    'constants', 'types', 'qt', 'table_widget', 'table_view',
    pytest.param('dummy', marks=pytest.mark.xfail)])
def test_module_imports(module_name):
    """Test modules import."""
    result = True
    try:
        importlib.import_module(f'qspreadsheet.{module_name}')
    except ImportError:
        result = False
    finally:
        assert result
