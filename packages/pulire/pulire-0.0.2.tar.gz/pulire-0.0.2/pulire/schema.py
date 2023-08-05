"""
PULIRE

Schema Class

The code is licensed under the MIT license.
"""

from copy import copy
from inspect import isfunction
from pandas import DataFrame, Series
from .validator import ValidationError, Validator


class Schema:
    """
    Pulire Schema
    """

    _columns: dict = {}  # The columns

    def __init__(self, columns: dict):
        self._columns = columns

    def columns(self) -> list:
        """
        Get the list of column names
        """
        return list(self._columns.values())

    @staticmethod
    def _run_check(validator: Validator, df: DataFrame, column: str = None) -> Series:
        validator = validator() if isfunction(validator) else validator
        if validator.skip_null:
            result = Series(data=True, index=df.index, dtype=bool)
            result.update(validator.check(df.loc[df[column].notnull()], column))
            return result.astype(bool)
        return validator.check(df, column)

    def validate(self, df: DataFrame, fill=None) -> DataFrame:
        """
        Validate a DataFrame
        """
        temp = copy(df)

        for name, validators in self._columns.items():
            if name in df.columns:
                for validator in validators:
                    test = self._run_check(validator, df, name)
                    temp.loc[~test, name] = fill

        return temp

    def debug(self, df: DataFrame) -> None:
        """
        Raise error when checks are failing
        """
        for name, validators in self._columns.items():
            if name in df.columns:
                for i, validator in enumerate(validators):
                    test = self._run_check(validator, df, name)
                    if not test.all():
                        raise ValidationError(name, i, df, test)

    def is_valid(self, df: DataFrame) -> bool:
        """
        Check if a DataFrame is valid
        """
        for name, validators in self._columns.items():
            if name in df.columns:
                for validator in validators:
                    test = self._run_check(validator, df, name)
                    if not test.all():
                        return False
        return True
