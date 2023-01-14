"""Custom type definitions for the qspreadsheet package."""
from datetime import datetime
from types import TracebackType
from typing import Tuple, Type, TypeVar, Union

import pandas

from qspreadsheet import qt

DF = TypeVar('DF', bound=pandas.DataFrame)
SER = TypeVar('SER', bound=pandas.Series)
ExcInfo = Tuple[Type[BaseException], BaseException, TracebackType]
DateLike = Union[str, datetime, pandas.Timestamp, qt.QDate]
