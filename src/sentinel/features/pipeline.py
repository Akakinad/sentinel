
"""Feature pipeline: builds every model feature in one place.

Training and the API both call build_features(), so features are always
computed the same way (no training-serving skew).
"""

import pandas as pd

from sentinel.features.behaviour import add_amount_features, add_count_features
from sentinel.features.geo import add_distance_feature
from sentinel.features.temporal import add_time_features

TIME_COL = "trans_date_trans_time"

# The fixed list of purchase categories seen in the data.
CATEGORIES = [
    "entertainment", "food_dining", "gas_transport", "grocery_net",
    "grocery_pos", "health_fitness", "home", "kids_pets", "misc_net",
    "misc_pos", "personal_care", "shopping_net", "shopping_pos", "travel",
]
CATEGORY_TYPE = pd.CategoricalDtype(categories=CATEGORIES)

# The exact columns the model is allowed to see.
FEATURE_COLUMNS = [
    "amt",
    "category",
    "city_pop",
    "hour",
    "is_night",
    "day_of_week",
    "distance_km",
    "tx_count_1h",
    "tx_count_24h",
    "tx_count_7d",
    "avg_amt_30d",
    "amt_ratio_30d",
]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with every model feature added, sorted by time."""
    out = add_time_features(df)
    out = add_distance_feature(out)
    out = add_count_features(out)
    out = add_amount_features(out)

    out["category"] = out["category"].astype(CATEGORY_TYPE)
    return out.sort_values(TIME_COL, kind="stable").reset_index(drop=True)
