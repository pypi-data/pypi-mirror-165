"""
PULIRE

The code is licensed under the MIT license.
"""

from typing import Union
from pandas import Series
from ..validator import Validator


def min(value: Union[int, float]) -> Series:
    """
    Numeric minimum
    """
    return Validator(lambda s: s >= value)
