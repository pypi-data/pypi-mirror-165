"""
PULIRE

The code is licensed under the MIT license.
"""

from pandas import Series
from ..validator import Validator


def isin(values: list) -> Series:
    """
    Require column value to be in a list of values
    """
    return Validator(lambda s: s.isin(values))
