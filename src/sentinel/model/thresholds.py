
"""Decision thresholds: chosen from the precision-recall curve."""

from sklearn.metrics import precision_recall_curve

TARGET_PRECISION = 0.95  # auto-block must be at least this precise
TARGET_RECALL = 0.95  # investigate + block must catch this share of fraud


def choose_thresholds(
    y_true,
    scores,
    target_precision: float = TARGET_PRECISION,
    target_recall: float = TARGET_RECALL,
) -> tuple[float, float]:
    """Return (low, high): investigate from low, block from high."""
    precision, recall, thresholds = precision_recall_curve(y_true, scores)
    precision, recall = precision[:-1], recall[:-1]

    high = thresholds[precision >= target_precision].min()
    low = thresholds[recall >= target_recall].max()
    if low >= high:
        raise ValueError(f"low threshold {low:.4f} is not below high {high:.4f}")
    return float(low), float(high)


def assign_zone(score: float, low: float, high: float) -> str:
    """Map one fraud score to 'approve', 'investigate' or 'block'."""
    if score >= high:
        return "block"
    if score >= low:
        return "investigate"
    return "approve"
