"""
PULIRE

Frequency Conversion Utility

The code is licensed under the MIT license.
"""

from pandas import DataFrame, date_range, concat


def as_freq(df: DataFrame, freq: str) -> DataFrame:
    """
    Convert time series to frequency
    """
    # Get time range
    start = df.index.min()
    end = df.index.max()

    # Result DataFrame
    result = DataFrame(columns=df.columns)
    result[df.index.name] = date_range(start, end, freq=freq)

    # Add columns
    for column in df.columns:
        # Add column to DataFrame
        result[column] = None

    # Set index
    result.set_index(df.index.name, inplace=True)

    # Return new instance
    return (
        concat(
            [df, result],
            axis=0,
        )
        .groupby(df.index.name, as_index=True)
        .first()
    )
