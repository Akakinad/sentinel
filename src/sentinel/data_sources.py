
"""Project paths and raw-data loading, defined once for every script."""

from pathlib import Path

import pandas as pd

# src/sentinel/data_sources.py -> parents[2] is the project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
MODEL_DIR = PROJECT_ROOT / "models"
HISTORY_DB_PATH = PROJECT_ROOT / "data" / "history.db"

RAW_FILES = ["fraudTrain.csv", "fraudTest.csv"]


def load_raw() -> pd.DataFrame:
    """Load and combine the two Sparkov CSVs; stop if they are missing."""
    for name in RAW_FILES:
        if not (RAW_DIR / name).exists():
            raise SystemExit(
                f"ERROR: {name} not found. Run scripts/download_data.py first."
            )
    tables = [pd.read_csv(RAW_DIR / name, index_col=0) for name in RAW_FILES]
    return pd.concat(tables, ignore_index=True)
