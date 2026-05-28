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


def test_validate_ok_without_valid_tags_allows_suggestions_only() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    payload = _load(os.path.join(FIXTURES_DIR, "payload_no_valid_tags.json"))
    output = {
        "metadata": payload["metadata"],
        "input_tags": payload["input_tags"],
        "remove_tags": [],
        "add_tags": [],
        "suggest_tags": [
            {"tag": "ai_task:detection", "note": "目标检测"},
            {"tag": "model:DL/DETR", "note": "DEtection TRansformer"},
            {"tag": "model:DL/Transformer", "note": "Transformer"},
        ],
        "provenance": {"generated_at": "2026-02-11T00:00:00Z"},
        "warnings": [],
        "error": None,
    }

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=payload)
    assert issues == []


def test_validate_rejects_add_tags_without_valid_tags() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    payload = _load(os.path.join(FIXTURES_DIR, "payload_no_valid_tags.json"))
    output = {
        "metadata": payload["metadata"],
        "input_tags": payload["input_tags"],
        "remove_tags": [],
        "add_tags": ["ai_task:detection"],
        "suggest_tags": [],
        "provenance": {"generated_at": "2026-02-11T00:00:00Z"},
        "warnings": [],
        "error": None,
    }

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=payload)
    assert any("add_tags must be empty when valid_tags is not provided" in i.message for i in issues)


def test_validate_rejects_invalid_suggest_tag_standard_shape() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    output = {
        "metadata": {"title": "x"},
        "input_tags": [],
        "remove_tags": [],
        "add_tags": [],
        "suggest_tags": [{"tag": "topic:bad tag", "note": "bad"}],
        "provenance": {"generated_at": "2026-02-11T00:00:00Z"},
        "warnings": [],
        "error": None,
    }

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=None)
    assert any("suggest_tags[].tag must not contain whitespace" in i.message for i in issues)


def test_validate_ok_with_missing_payload_input_tags_echoes_empty_list() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    payload = {"metadata": {"title": "Object detection with DETR"}, "infer_tag": True}
    output = {
        "metadata": payload["metadata"],
        "input_tags": [],
        "remove_tags": [],
        "add_tags": [],
        "suggest_tags": [
            {"tag": "ai_task:detection", "note": "目标检测"},
            {"tag": "model:DL/DETR", "note": "DEtection TRansformer"},
        ],
        "provenance": {"generated_at": "2026-02-11T00:00:00Z"},
        "warnings": [],
        "error": None,
    }

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=payload)
    assert issues == []


def test_validate_rejects_missing_payload_input_tags_wrong_echo() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    payload = {"metadata": {"title": "Object detection with DETR"}}
    output = {
        "metadata": payload["metadata"],
        "input_tags": ["unexpected"],
        "remove_tags": [],
        "add_tags": [],
        "suggest_tags": [],
        "provenance": {"generated_at": "2026-02-11T00:00:00Z"},
        "warnings": [],
        "error": None,
    }

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=payload)
    assert any("output input_tags does not match payload input_tags" in i.message for i in issues)


def test_validate_ok_insufficient_input_error() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    output = {
        "metadata": None,
        "input_tags": [],
        "remove_tags": [],
        "add_tags": [],
        "suggest_tags": [],
        "provenance": {"generated_at": "2026-02-11T00:00:00Z"},
        "warnings": [],
        "error": {
            "type": "insufficient_input",
            "message": "No metadata, digest_markdown, input_tags, or valid_tags evidence was provided",
        },
    }

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data={})
    assert issues == []


def test_validate_ok_digest_only_inference_without_metadata() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    payload = {"digest_markdown": "/abs/path/to/digest.md", "infer_tag": True}
    output = {
        "metadata": None,
        "input_tags": [],
        "remove_tags": [],
        "add_tags": [],
        "suggest_tags": [{"tag": "ai_task:detection", "note": "目标检测"}],
        "provenance": {"generated_at": "2026-02-11T00:00:00Z"},
        "warnings": [],
        "error": None,
    }

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=payload)
    assert issues == []


def test_validate_ok_pure_inference_with_false_infer_tag() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    payload = {"metadata": {"title": "Object detection with DETR"}, "input_tags": [], "infer_tag": False}
    output = {
        "metadata": payload["metadata"],
        "input_tags": [],
        "remove_tags": [],
        "add_tags": [],
        "suggest_tags": [{"tag": "ai_task:detection", "note": "目标检测"}],
        "provenance": {"generated_at": "2026-02-11T00:00:00Z"},
        "warnings": ["纯推断模式下已忽略 infer_tag=false，以避免无输出"],
        "error": None,
    }

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=payload)
    assert issues == []


def test_validate_ok_controlled_normalization_with_false_infer_tag() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    payload = {
        "metadata": {"title": "unused"},
        "input_tags": ["tool:pytorch"],
        "valid_tags": ["tool:PyTorch"],
        "infer_tag": False,
    }
    output = {
        "metadata": payload["metadata"],
        "input_tags": payload["input_tags"],
        "remove_tags": ["tool:pytorch"],
        "add_tags": ["tool:PyTorch"],
        "suggest_tags": [],
        "provenance": {"generated_at": "2026-02-11T00:00:00Z"},
        "warnings": [],
        "error": None,
    }

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=payload)
    assert issues == []


def test_validate_rejects_tag_note_language_scope_leak() -> None:
    schema = _load(os.path.join(ASSETS_DIR, "output_schema.json"))
    output = _load(os.path.join(FIXTURES_DIR, "output_invalid_scope_leak_tag_note_language.json"))

    issues = validate_output_data(output_data=output, schema_data=schema, payload_data=None)
    assert any("must not appear in output" in i.message for i in issues)
