
"""Location features: distance from the customer's home to the merchant."""

import numpy as np
import pandas as pd

EARTH_RADIUS_KM = 6_371.0


def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance in km between points given in degrees.

    Works on single numbers or on whole columns at once.
    """
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * np.arcsin(np.sqrt(a))


def add_distance_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with distance_km (customer home to merchant) added."""
    out = df.copy()
    out["distance_km"] = haversine_km(
        out["lat"], out["long"], out["merch_lat"], out["merch_long"]
    )
    return out
