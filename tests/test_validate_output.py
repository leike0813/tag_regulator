from __future__ import annotations

import json
import os
import sys
from typing import Any


REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "dev-tools", "tag-regulator", "scripts")
ASSETS_DIR = os.path.join(REPO_ROOT, "dev-tools", "tag-regulator", "assets")
FIXTURES_DIR = os.path.join(REPO_ROOT, "tests", "fixtures")

sys.path.insert(0, SCRIPTS_DIR)

from validate_output import validate_output_data  # noqa: E402


def _load(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_validate_ok() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    payload = _load(os.path.join(FIXTURES_DIR, "payload_basic.json"))
    output = _load(os.path.join(FIXTURES_DIR, "output_basic_valid.json"))

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=payload)
    assert issues == []


def test_validate_ok_with_valid_tags_file() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    payload = _load(os.path.join(FIXTURES_DIR, "payload_no_valid_tags.json"))
    output = _load(os.path.join(FIXTURES_DIR, "output_no_valid_tags_valid.json"))

    from validate_output import load_valid_tags_from_file  # noqa: E402

    valid_tags = load_valid_tags_from_file(path=os.path.join(FIXTURES_DIR, "valid_tags.yaml"), fmt="yaml")
    payload = dict(payload)
    payload["valid_tags"] = valid_tags

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=payload)
    assert issues == []


def test_validate_rejects_add_not_in_valid_tags() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    payload = _load(os.path.join(FIXTURES_DIR, "payload_basic.json"))
    output = _load(os.path.join(FIXTURES_DIR, "output_invalid_add_not_in_valid.json"))

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=payload)
    assert any("add tag not present in valid_tags" in i.message for i in issues)


def test_validate_rejects_remove_not_in_input_tags() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    output = _load(os.path.join(FIXTURES_DIR, "output_invalid_remove_not_in_input.json"))

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=None)
    assert any("remove tag not present in input_tags" in i.message for i in issues)
