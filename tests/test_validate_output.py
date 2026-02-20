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


def test_validate_ok_with_tag_note_language_scope() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    payload = _load(os.path.join(FIXTURES_DIR, "payload_basic_with_note_language.json"))
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


def test_validate_rejects_suggest_duplicate_tag() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    output = _load(os.path.join(FIXTURES_DIR, "output_invalid_suggest_duplicate_tag.json"))

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=None)
    assert any("suggest_tags[].tag must not contain duplicates" in i.message for i in issues)


def test_validate_rejects_suggest_invalid_shape() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    output = _load(os.path.join(FIXTURES_DIR, "output_invalid_suggest_shape.json"))

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=None)
    assert any("is a required property" in i.message for i in issues)


def test_validate_rejects_suggest_tag_in_valid_tags() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    payload = _load(os.path.join(FIXTURES_DIR, "payload_basic.json"))
    output = _load(os.path.join(FIXTURES_DIR, "output_invalid_suggest_in_valid_tags.json"))

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=payload)
    assert any("suggest tag MUST NOT be in valid_tags" in i.message for i in issues)


def test_validate_rejects_tag_note_language_scope_leak() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    output = _load(os.path.join(FIXTURES_DIR, "output_invalid_scope_leak_tag_note_language.json"))

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=None)
    assert any("must not appear in output" in i.message for i in issues)
