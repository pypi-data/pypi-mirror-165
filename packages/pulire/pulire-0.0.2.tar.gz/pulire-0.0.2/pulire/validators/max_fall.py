"""
PULIRE

The code is licensed under the MIT license.
"""

from typing import Union
from pandas import Series
from ..validator import Validator


def max_fall(value: Union[int, float]) -> Series:
    """
    Maximum decrease compared to previous value
    """

    def _func(s: Series):
        result = Series(data=0, index=s.index)
        result.update(s.iloc[1:].diff().notnull())
        return result >= value * -1

    return Validator(_func, skip_null=False)
