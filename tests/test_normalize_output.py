from __future__ import annotations

import json
import os
import sys
from typing import Any


REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "tag-regulator", "scripts")
FIXTURES_DIR = os.path.join(REPO_ROOT, "tests", "fixtures")

sys.path.insert(0, SCRIPTS_DIR)

from normalize_output import normalize_output_data  # noqa: E402


def _load(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_normalize_dedup_and_ordering() -> None:
    raw = _load(os.path.join(FIXTURES_DIR, "output_needs_normalize.json"))
    expected = _load(os.path.join(FIXTURES_DIR, "output_normalized_expected.json"))
    assert normalize_output_data(raw) == expected

