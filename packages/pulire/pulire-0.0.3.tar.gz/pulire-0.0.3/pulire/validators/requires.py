"""
PULIRE

The code is licensed under the MIT license.
"""

from pandas import Series
from ..validator import Validator


def requires(column: str) -> Series:
    """
    Require another column not to be null
    """
    return Validator(lambda _, s: s[column].notna(), skip_null=False)
