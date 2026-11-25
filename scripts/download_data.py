
"""Download the Sparkov fraud dataset from Kaggle into data/raw/.

Usage:
    uv run python scripts/download_data.py
"""

from pathlib import Path

# --- Configuration ---------------------------------------------------------

# Kaggle dataset ID: "<owner>/<dataset-name>"
DATASET_ID = "kartik2112/fraud-detection"

# Project root = the folder that contains scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Where the raw CSVs are saved (git-ignored via data/)
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Exact file sizes in bytes, from `kaggle datasets files`
EXPECTED_FILES = {
    "fraudTrain.csv": 351_238_196,
    "fraudTest.csv": 150_354_339,
}

# --- Steps -----------------------------------------------------------------


def files_already_present() -> bool:
    """Return True if every expected CSV exists with its exact expected size."""
    for name, expected_size in EXPECTED_FILES.items():
        path = RAW_DIR / name
        if not path.exists() or path.stat().st_size != expected_size:
            return False
    return True

def download_dataset() -> None:
    """Download the dataset from Kaggle and unzip it into RAW_DIR."""
    # Imported here, not at the top, so the file check above
    # works even on a machine without Kaggle credentials.
    from kaggle.api.kaggle_api_extended import KaggleApi

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    api = KaggleApi()
    api.authenticate()
    print(f"Downloading {DATASET_ID} into {RAW_DIR} ...")
    api.dataset_download_files(DATASET_ID, path=str(RAW_DIR), unzip=True, quiet=False)

def verify_files() -> None:
    """Stop with an error unless every expected CSV exists with its exact size."""
    for name, expected_size in EXPECTED_FILES.items():
        path = RAW_DIR / name
        if not path.exists():
            raise SystemExit(f"ERROR: {name} is missing from {RAW_DIR}")
        actual_size = path.stat().st_size
        if actual_size != expected_size:
            raise SystemExit(
                f"ERROR: {name} is {actual_size:,} bytes, expected {expected_size:,}"
            )
        print(f"OK  {name}  ({actual_size:,} bytes)")

def main() -> None:
    """Download the dataset unless it is already present, then verify it."""
    if files_already_present():
        print(f"Dataset already present in {RAW_DIR}, skipping download.")
    else:
        download_dataset()
    verify_files()


if __name__ == "__main__":
    main()
