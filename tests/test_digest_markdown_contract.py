from __future__ import annotations

import json
import os
from typing import Any


REPO_ROOT = os.path.dirname(os.path.dirname(__file__))


def _load(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_input_schema_accepts_optional_digest_markdown() -> None:
    schema = _load(os.path.join(REPO_ROOT, "tag-regulator", "assets", "input.schema.json"))
    props = schema["properties"]
    assert "digest_markdown" in props
    digest = props["digest_markdown"]
    assert digest["type"] == "string"
    assert digest["x-input-source"] == "file"
    assert ".md" in digest["extensions"]
    assert "digest_markdown" not in schema.get("required", [])


def test_input_schema_accepts_optional_valid_tags() -> None:
    schema = _load(os.path.join(REPO_ROOT, "tag-regulator", "assets", "input.schema.json"))
    props = schema["properties"]
    assert "valid_tags" in props
    assert props["valid_tags"]["x-input-source"] == "file"
    assert "pure inference mode" in props["valid_tags"]["description"]
    assert "valid_tags" not in schema.get("required", [])


def test_input_schema_accepts_optional_input_tags() -> None:
    schema = _load(os.path.join(REPO_ROOT, "tag-regulator", "assets", "input.schema.json"))
    props = schema["properties"]
    assert "input_tags" in props
    assert "Missing input_tags is treated as an empty array" in props["input_tags"]["description"]
    assert "input_tags" not in schema.get("required", [])


def test_runner_prompt_includes_digest_markdown_placeholder() -> None:
    runner = _load(os.path.join(REPO_ROOT, "tag-regulator", "assets", "runner.json"))
    prompt = runner["entrypoint"]["prompts"]["common"]
    assert "digest_markdown={{ input.digest_markdown }}" in prompt
    assert "optional" in prompt


def test_runner_prompt_marks_valid_tags_optional() -> None:
    runner = _load(os.path.join(REPO_ROOT, "tag-regulator", "assets", "runner.json"))
    prompt = runner["entrypoint"]["prompts"]["common"]
    assert "valid_tags={{ input.valid_tags }} (optional" in prompt
    assert "pure inference mode" in prompt


def test_parameter_schema_describes_infer_tag_evidence_gating() -> None:
    schema = _load(os.path.join(REPO_ROOT, "tag-regulator", "assets", "parameter.schema.json"))
    description = schema["properties"]["infer_tag"]["description"]
    assert "metadata/digest-driven supplemental inference" in description
    assert "pure inference mode" in description


def test_skill_mentions_digest_markdown_optional_behavior() -> None:
    path = os.path.join(REPO_ROOT, "tag-regulator", "SKILL.md")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    assert "{{ input.digest_markdown }}" in text
    assert "不可读/编码异常时记录 `warnings` 后忽略" in text
    assert "可读非空 `digest_markdown`" in text
    assert "insufficient_input" in text
