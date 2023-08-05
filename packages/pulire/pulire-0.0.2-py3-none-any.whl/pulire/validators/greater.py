"""
PULIRE

The code is licensed under the MIT license.
"""

from pandas import Series
from ..validator import Validator


def greater(column: str) -> Series:
    """
    Require column to be greather than another one
    """

    def _func(series, df, name):
        result = Series(data=True, index=series.index)
        df = df[df[name].notnull() & df[column].notnull()]
        result.update(df[name] > df[column])
        return result.astype(bool)

    return Validator(_func, skip_null=False)
