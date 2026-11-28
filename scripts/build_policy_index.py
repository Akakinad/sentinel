
"""Build the policy vector index (data/policy_index) from the policy manual.

Usage:
    uv run python scripts/build_policy_index.py
"""

from sentinel.data_sources import POLICY_INDEX_DIR, POLICY_MANUAL_PATH
from sentinel.rag.index import build_policy_index
from sentinel.rag.policies import load_policies


def main() -> None:
    """Split the manual into policies and store them with their embeddings."""
    policies = load_policies(POLICY_MANUAL_PATH)
    print(f"Loaded {len(policies)} policies from {POLICY_MANUAL_PATH.name}")

    stored = build_policy_index(policies, POLICY_INDEX_DIR)
    print(f"Indexed {stored} policies into {POLICY_INDEX_DIR}")


if __name__ == "__main__":
    main()
