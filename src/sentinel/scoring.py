
"""Score one incoming transaction the way production does."""

import sqlite3

import lightgbm as lgb
import pandas as pd

from sentinel.features.pipeline import FEATURE_COLUMNS, build_features
from sentinel.model.thresholds import assign_zone
from sentinel.storage.history import fetch_customer_history

TIME_COL = "trans_date_trans_time"
HISTORY_DAYS = 30  # covers the longest rolling window (avg_amt_30d)


def build_online_features(conn: sqlite3.Connection, tx: dict) -> pd.DataFrame:
    """Compute one transaction's features from its customer's stored history.

    Returns a one-row table with every feature column.
    """
    history = fetch_customer_history(conn, tx["cc_num"], tx[TIME_COL], days=HISTORY_DAYS)
    frame = pd.concat([history, pd.DataFrame([tx])], ignore_index=True)
    features = build_features(frame)
    return features[features["trans_num"] == tx["trans_num"]]


def score_transaction(
    conn: sqlite3.Connection, tx: dict, booster: lgb.Booster, metadata: dict
) -> dict:
    """Return the fraud score, the decision zone and the features used."""
    row = build_online_features(conn, tx)
    score = float(booster.predict(row[FEATURE_COLUMNS])[0])
    zone = assign_zone(score, metadata["low_threshold"], metadata["high_threshold"])
    return {
        "trans_num": tx["trans_num"],
        "score": score,
        "zone": zone,
        "features": row[FEATURE_COLUMNS].iloc[0].to_dict(),
    }
