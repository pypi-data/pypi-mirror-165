"""
PULIRE

The code is licensed under the MIT license.
"""

from typing import Union
from pandas import Series
from scipy.signal import find_peaks, peak_prominences
from ..validator import Validator


def max_peak(value: Union[int, float]) -> Series:
    """
    Maximum peak in a time series
    """

    def _func(series):
        result = Series(data=0, index=series.index)
        peaks, _ = find_peaks(series.values)
        prominences = peak_prominences(series.values, peaks, 2)[0]
        result.iloc[peaks] = prominences
        return result < value

    return Validator(_func, skip_null=False)
