"""
PULIRE

The code is licensed under the MIT license.
"""

from pandas import Series
from ..validator import Validator


def regex(pattern: str) -> Series:
    """
    Check if column values match regex pattern
    """
    return Validator(lambda s: s.str.contains(pattern))
