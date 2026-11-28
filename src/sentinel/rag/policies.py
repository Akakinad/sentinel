
"""Policy manual: split into one chunk per policy."""

import re
from dataclasses import dataclass
from pathlib import Path

# Matches lines like "## POL-003 Unusual amount for the customer"
POLICY_HEADING = re.compile(r"^## (POL-\d{3}) (.+)$", re.MULTILINE)


@dataclass(frozen=True)
class Policy:
    """One policy from the manual."""

    policy_id: str
    title: str
    text: str


def load_policies(path: Path) -> list[Policy]:
    """Split the manual at each '## POL-xxx' heading: one Policy per section."""
    manual = path.read_text(encoding="utf-8")
    headings = list(POLICY_HEADING.finditer(manual))

    policies = []
    for i, heading in enumerate(headings):
        end = headings[i + 1].start() if i + 1 < len(headings) else len(manual)
        body = manual[heading.end():end].strip()
        policies.append(Policy(heading.group(1), heading.group(2).strip(), body))
    return policies
