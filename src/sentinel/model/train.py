
"""Train the LightGBM fraud model with early stopping on the validation set."""

import lightgbm as lgb
import pandas as pd

from sentinel.features.pipeline import FEATURE_COLUMNS

TARGET_COL = "is_fraud"
RANDOM_SEED = 42

BASE_PARAMS = {
    "objective": "binary",
    "metric": "average_precision",
    "n_estimators": 2000,
    "learning_rate": 0.05,
    "num_leaves": 31,
    "min_child_samples": 100,
    "subsample": 0.8,
    "subsample_freq": 1,
    "colsample_bytree": 0.8,
    "random_state": RANDOM_SEED,
    "verbose": -1,
}


def train_model(
    train: pd.DataFrame, validate: pd.DataFrame, weight_fraud: bool = False
) -> lgb.LGBMClassifier:
    """Train on train; stop adding trees when validation PR-AUC stops improving."""
    params = dict(BASE_PARAMS)
    if weight_fraud:
        n_legit = (train[TARGET_COL] == 0).sum()
        n_fraud = (train[TARGET_COL] == 1).sum()
        params["scale_pos_weight"] = n_legit / n_fraud

    model = lgb.LGBMClassifier(**params)
    model.fit(
        train[FEATURE_COLUMNS],
        train[TARGET_COL],
        eval_X=validate[FEATURE_COLUMNS],
        eval_y=validate[TARGET_COL],
        callbacks=[lgb.early_stopping(stopping_rounds=100, verbose=False)],
    )
    return model
