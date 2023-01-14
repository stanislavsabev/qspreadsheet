"""Logging wrapper."""

import logging


def getLogger(name: str):
    """Registers and returns logger with given name.

    Args:
        name (str): Logger name.

    Returns:
        Logger: Registered logger with given name.
    """
    return logging.getLogger(name)