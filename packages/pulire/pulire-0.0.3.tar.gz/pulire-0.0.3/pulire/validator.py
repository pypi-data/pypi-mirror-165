"""
PULIRE

Validator Class

The code is licensed under the MIT license.
"""

from inspect import signature
from typing import Callable, Union
from pandas import DataFrame, Series


class Validator:
    """
    Series Validator
    """

    func: Union[Callable, None] = None
    vectorized: bool = True
    skip_null: bool = False

    def __init__(self, func: Callable, vectorized: bool = True, skip_null=True):
        self.func = func
        self.vectorized = vectorized
        self.skip_null = skip_null

    def check(self, df: DataFrame, column: str) -> Union[bool, Series]:
        """
        Run validator

        Returns a bool series:
        True -> Check passed
        False -> Check failed
        """
        arg_count = len((signature(self.func)).parameters)
        args = [df[column] if column else df, df, column]
        if self.vectorized:
            return self.func(*args[0:arg_count])
        raise NotImplementedError("Pulire doesn't support non-vectorized checks, yet.")


class ValidationError(Exception):
    """
    Exception which is raised when a validation fails
    """

    column: str = None
    validator: int = None
    errors: DataFrame = None

    def __init__(self, column: str, validator: int, df: DataFrame, test: Series):
        super().__init__(
            f"Validator [{validator}] failing for column '{column}' on the following rows:\n"
            f"{df[~test]}"
        )

        self.column = column
        self.validator = validator
        self.errors = df[~test]
