"""
PULIRE

Column Class

The code is licensed under the MIT license.
"""

from typing import Union


class Column:
    """
    Generic Column
    """

    name: Union[str, None] = None
    dtype: Union[type, str, None] = None
    validators: list = []

    def __init__(
        self,
        name: str,
        dtype: Union[type, str, None] = None,
        validators: Union[list, None] = None,
    ):
        self.name = name
        self.dtype = dtype
        if isinstance(validators, list):
            self.validators = validators
