
"""Behaviour features: per-customer activity in past time windows."""

import pandas as pd

CUSTOMER_COL = "cc_num"
TIME_COL = "trans_date_trans_time"

# Feature name -> window length (pandas time strings)
COUNT_WINDOWS = {
    "tx_count_1h": "1h",
    "tx_count_24h": "24h",
    "tx_count_7d": "7D",
}


def add_count_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with per-customer transaction counts in past windows.

    Each window ends just before the current transaction (closed="left"),
    so a transaction never counts itself or anything after it.
    The result is sorted by customer, then time.
    """
    out = df.copy()
    out[TIME_COL] = pd.to_datetime(out[TIME_COL])
    out = out.sort_values([CUSTOMER_COL, TIME_COL])

    grouped = out.set_index(TIME_COL).groupby(CUSTOMER_COL)["amt"]

    for name, window in COUNT_WINDOWS.items():
        counts = grouped.rolling(window, closed="left").count()
        out[name] = counts.fillna(0).astype(int).to_numpy()

    return out

AMOUNT_WINDOW = "30D"


def add_amount_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add each customer's past 30-day average amount and the ratio to it.

    The window ends just before the current transaction (closed="left").
    With no purchase in the previous 30 days, both values are NaN.
    The result is sorted by customer, then time.
    """
    out = df.copy()
    out[TIME_COL] = pd.to_datetime(out[TIME_COL])
    out = out.sort_values([CUSTOMER_COL, TIME_COL])

    grouped = out.set_index(TIME_COL).groupby(CUSTOMER_COL)["amt"]
    out["avg_amt_30d"] = grouped.rolling(AMOUNT_WINDOW, closed="left").mean().to_numpy()
    out["amt_ratio_30d"] = out["amt"] / out["avg_amt_30d"]
    return out
