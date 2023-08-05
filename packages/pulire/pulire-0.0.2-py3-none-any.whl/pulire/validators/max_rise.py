"""
PULIRE

The code is licensed under the MIT license.
"""

from typing import Union
from pandas import Series
from ..validator import Validator


def max_rise(value: Union[int, float]) -> Series:
    """
    Maximum increase compared to previous value
    """

    def _func(s: Series):
        result = Series(data=0, index=s.index)
        result.update(s.iloc[1:].diff().notnull())
        return result <= value

    return Validator(_func, skip_null=False)
