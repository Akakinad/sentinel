
"""Train the fraud model end to end and save it to models/.

Usage:
    uv run python scripts/train_model.py
"""

from pathlib import Path

import pandas as pd
from sklearn.metrics import average_precision_score

from sentinel.features.pipeline import CATEGORIES, FEATURE_COLUMNS, build_features
from sentinel.model.artifacts import save_model
from sentinel.model.split import SPLITS, split_by_time
from sentinel.model.thresholds import choose_thresholds
from sentinel.model.train import TARGET_COL, train_model

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
MODEL_DIR = PROJECT_ROOT / "models"
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


def main() -> None:
    """Run every step from raw data to a saved model."""
    print("1/5 Loading raw data ...")
    df = load_raw()

    print("2/5 Building features and splitting by time ...")
    parts = split_by_time(build_features(df))
    train, validate, test = parts["train"], parts["validate"], parts["test"]

    print("3/5 Training LightGBM ...")
    booster = train_model(train, validate).booster_

    print("4/5 Choosing thresholds and evaluating ...")
    val_scores = booster.predict(validate[FEATURE_COLUMNS])
    test_scores = booster.predict(test[FEATURE_COLUMNS])
    low, high = choose_thresholds(validate[TARGET_COL], val_scores)

    metadata = {
        "low_threshold": low,
        "high_threshold": high,
        "feature_columns": FEATURE_COLUMNS,
        "categories": CATEGORIES,
        "best_iteration": int(booster.best_iteration),
        "trained_on": " to ".join(SPLITS["train"]),
        "validation_pr_auc": round(float(average_precision_score(validate[TARGET_COL], val_scores)), 4),
        "test_pr_auc": round(float(average_precision_score(test[TARGET_COL], test_scores)), 4),
    }

    print("5/5 Saving model ...")
    save_model(booster, metadata, MODEL_DIR)

    print(f"Done. Saved to {MODEL_DIR}")
    for key in ("best_iteration", "low_threshold", "high_threshold",
                "validation_pr_auc", "test_pr_auc"):
        print(f"  {key}: {metadata[key]}")


if __name__ == "__main__":
    main()
