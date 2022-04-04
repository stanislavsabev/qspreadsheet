"""Test for the TableWidget object."""


def test_create(cls, *args, **kwargs):
    """Util to test creation of objects."""
    obj = cls(*args, **kwargs)
    assert obj is not None
