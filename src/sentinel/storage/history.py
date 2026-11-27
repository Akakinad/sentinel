
"""Transaction history database (SQLite): seeded once, then grown by the replay."""

import sqlite3
from pathlib import Path

import pandas as pd

TABLE = "transactions"
TIME_COL = "trans_date_trans_time"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"  # text that sorts in time order

# Only what scoring and the agent need; personal fields stay out.
COLUMNS = [
    "trans_num", "cc_num", TIME_COL, "amt", "category", "merchant",
    "city_pop", "lat", "long", "merch_lat", "merch_long", "is_fraud",
]


def create_history_db(df: pd.DataFrame, db_path: Path, before: str) -> int:
    """Create a fresh database with every transaction before `before`.

    Returns the number of rows written.
    """
    times = pd.to_datetime(df[TIME_COL])
    history = df.loc[times < before, COLUMNS].copy()
    history[TIME_COL] = pd.to_datetime(history[TIME_COL]).dt.strftime(TIME_FORMAT)

    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_path.unlink(missing_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        history.to_sql(TABLE, conn, index=False)
        conn.execute(f"CREATE UNIQUE INDEX idx_trans_num ON {TABLE} (trans_num)")
        conn.execute(
            f"CREATE INDEX idx_customer_time ON {TABLE} (cc_num, {TIME_COL})"
        )
        conn.commit()
    finally:
        conn.close()
    return len(history)
