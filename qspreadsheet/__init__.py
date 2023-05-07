from typing import TypeVar

import pandas as _pd

from . import resources_rc

MAX_INT = 2147483647
MAX_FLOAT = 3.4028234664e+38
LEFT, ABOVE = range(2)

DF = TypeVar('DF', bound=_pd.DataFrame)
SER = TypeVar('SER', bound=_pd.Series)
