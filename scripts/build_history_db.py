
"""Build the transaction history database (data/history.db).

Seeds it with every transaction before the replay period starts.

Usage:
    uv run python scripts/build_history_db.py
"""

from sentinel.data_sources import HISTORY_DB_PATH, load_raw
from sentinel.model.split import SPLITS
from sentinel.storage.history import create_history_db


def main() -> None:
    """Load the raw data and write everything before the replay into SQLite."""
    replay_start = SPLITS["replay"][0]

    print("Loading raw data ...")
    df = load_raw()

    print(f"Writing transactions before {replay_start} to {HISTORY_DB_PATH} ...")
    rows = create_history_db(df, HISTORY_DB_PATH, before=replay_start)

    print(f"Done: {rows:,} transactions in the history database.")


if __name__ == "__main__":
    main()
