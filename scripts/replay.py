
"""Replay July-December 2020 through the scorer, one transaction at a time.

Each transaction is scored using only the history before it, then stored
together with its decision: both or neither.

Usage:
    uv run python scripts/replay.py               # next 2,000 transactions
    uv run python scripts/replay.py --limit 500   # choose how many
"""

import argparse
import sqlite3
import time

import pandas as pd

from sentinel.data_sources import HISTORY_DB_PATH, MODEL_DIR, load_raw
from sentinel.model.artifacts import load_model
from sentinel.model.split import SPLITS
from sentinel.scoring import score_transaction
from sentinel.storage.history import (
    DECISIONS_TABLE,
    add_transaction,
    ensure_decisions_table,
    record_decision,
)

TIME_COL = "trans_date_trans_time"
DEFAULT_LIMIT = 2_000


def pending_transactions(df: pd.DataFrame, conn: sqlite3.Connection) -> pd.DataFrame:
    """Replay-period transactions without a decision yet, oldest first."""
    start, end = SPLITS["replay"]
    times = pd.to_datetime(df[TIME_COL])
    replay = df[(times >= start) & (times < end)].copy()
    replay = replay.iloc[pd.to_datetime(replay[TIME_COL]).argsort(kind="stable")]

    done = {row[0] for row in conn.execute(f"SELECT trans_num FROM {DECISIONS_TABLE}")}
    return replay[~replay["trans_num"].isin(done)]


def main() -> None:
    """Score the next pending transactions and store each with its decision."""
    parser = argparse.ArgumentParser(description="Replay transactions through the scorer.")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                        help="how many transactions to replay this run")
    args = parser.parse_args()

    if not HISTORY_DB_PATH.exists():
        raise SystemExit("ERROR: no history database. Run scripts/build_history_db.py first.")

    booster, meta = load_model(MODEL_DIR)
    print("Loading raw data ...")
    df = load_raw()

    conn = sqlite3.connect(HISTORY_DB_PATH)
    try:
        ensure_decisions_table(conn)
        todo = pending_transactions(df, conn).head(args.limit)
        print(f"Replaying {len(todo):,} transactions ...")

        counts = {"approve": 0, "investigate": 0, "block": 0}
        started = time.perf_counter()
        for i, (_, row) in enumerate(todo.iterrows(), start=1):
            tx = row.to_dict()
            result = score_transaction(conn, tx, booster, meta)

            with conn:  # both writes are saved together, or neither
                add_transaction(conn, tx)
                record_decision(conn, tx, result["score"], result["zone"])

            counts[result["zone"]] += 1
            if i % 500 == 0:
                print(f"  {i:,} done")
        elapsed = time.perf_counter() - started
    finally:
        conn.close()

    print(f"Done in {elapsed:.1f}s ({1000 * elapsed / max(len(todo), 1):.1f} ms per transaction)")
    for zone, n in counts.items():
        print(f"  {zone:<12} {n:,}")


if __name__ == "__main__":
    main()
