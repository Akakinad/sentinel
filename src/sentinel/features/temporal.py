
"""Time-based features: hour of day, night flag and day of week."""

import pandas as pd

# Night window found in exploration: fraud rate is ~13-25x higher
# between 22:00 and 03:59 than during the day.
NIGHT_START_HOUR = 22
NIGHT_END_HOUR = 4  # exclusive: 04:00 is no longer night


def add_time_features(
    df: pd.DataFrame, time_col: str = "trans_date_trans_time"
) -> pd.DataFrame:
    """Return a copy of df with hour, is_night and day_of_week added."""
    out = df.copy()
    timestamps = pd.to_datetime(out[time_col])

    out["hour"] = timestamps.dt.hour
    out["is_night"] = (
        (out["hour"] >= NIGHT_START_HOUR) | (out["hour"] < NIGHT_END_HOUR)
    ).astype(int)
    out["day_of_week"] = timestamps.dt.dayofweek
    return out
