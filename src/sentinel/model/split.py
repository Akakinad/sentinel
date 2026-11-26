
"""Time-based split: train on the past, evaluate on the future."""

import pandas as pd

TIME_COL = "trans_date_trans_time"

# Each part covers [start, end): start included, end excluded,
# so no transaction falls into two parts or into a gap.
SPLITS = {
    "train": ("2019-01-01", "2020-01-01"),
    "validate": ("2020-01-01", "2020-04-01"),
    "test": ("2020-04-01", "2020-07-01"),
    "replay": ("2020-07-01", "2021-01-01"),
}


def split_by_time(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Split df into train, validate, test and replay parts by date."""
    times = pd.to_datetime(df[TIME_COL])
    parts = {}
    for name, (start, end) in SPLITS.items():
        in_range = (times >= start) & (times < end)
        parts[name] = df[in_range]
    return parts
