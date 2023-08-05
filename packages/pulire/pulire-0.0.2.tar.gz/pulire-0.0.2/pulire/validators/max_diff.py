"""
PULIRE

The code is licensed under the MIT license.
"""

from typing import Union
from pandas import Series
from ..validator import Validator


def max_diff(value: Union[int, float]) -> Series:
    """
    Maximum difference compared to previous value
    """

    def _func(s: Series):
        result = Series(data=0, index=s.index)
        result.update(s.iloc[1:].diff().notnull().abs())
        return result <= value

    return Validator(_func, skip_null=False)
