
"""Save and load the trained model together with its metadata."""

import json
from pathlib import Path

import lightgbm as lgb

MODEL_FILE = "model.txt"
METADATA_FILE = "metadata.json"


def save_model(booster: lgb.Booster, metadata: dict, model_dir: Path) -> None:
    """Write model.txt (the trees) and metadata.json (how to use them)."""
    model_dir.mkdir(parents=True, exist_ok=True)
    booster.save_model(str(model_dir / MODEL_FILE))
    with open(model_dir / METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=2)


def load_model(model_dir: Path) -> tuple[lgb.Booster, dict]:
    """Read the trees and their metadata back from model_dir."""
    booster = lgb.Booster(model_file=str(model_dir / MODEL_FILE))
    with open(model_dir / METADATA_FILE) as f:
        metadata = json.load(f)
    return booster, metadata
