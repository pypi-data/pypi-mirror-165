"""
PULIRE

Index Class

The code is licensed under the MIT license.
"""

from typing import Union


class Index:
    """
    Index Column
    """

    name: Union[str, None] = None
    dtype: Union[type, str, None] = None

    def __init__(self, name: str, dtype: Union[type, str, None] = None):
        self.name = name
        self.dtype = dtype
