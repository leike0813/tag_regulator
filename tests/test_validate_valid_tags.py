from __future__ import annotations

import os
import sys
from pathlib import Path


REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "tag-regulator", "scripts")

sys.path.insert(0, SCRIPTS_DIR)

from validate_valid_tags import load_valid_tags_from_file, main  # noqa: E402


def test_validate_valid_tags_yaml_ok(tmp_path: Path) -> None:
    path = tmp_path / "valid_tags.yaml"
    path.write_text("- field:CS/AI/CV\n- model:DL/Transformer\n", encoding="utf-8")

    tags, detected_format = load_valid_tags_from_file(path=str(path), fmt="yaml")
    assert tags == ["field:CS/AI/CV", "model:DL/Transformer"]
    assert detected_format == "yaml"


def test_validate_valid_tags_json_ok(tmp_path: Path) -> None:
    path = tmp_path / "valid_tags.json"
    path.write_text('["field:CS/AI/CV", "task:object-detection"]\n', encoding="utf-8")

    tags, detected_format = load_valid_tags_from_file(path=str(path), fmt="json")
    assert tags == ["field:CS/AI/CV", "task:object-detection"]
    assert detected_format == "json"


def test_validate_valid_tags_rejects_non_string_array(tmp_path: Path) -> None:
    path = tmp_path / "valid_tags.yaml"
    path.write_text("- field:CS/AI/CV\n- 123\n", encoding="utf-8")

    try:
        load_valid_tags_from_file(path=str(path), fmt="yaml")
        raise AssertionError("expected ValueError for non-string array item")
    except ValueError as exc:
        assert "top-level list of strings" in str(exc)


def test_validate_valid_tags_rejects_non_array_content(tmp_path: Path) -> None:
    path = tmp_path / "valid_tags.json"
    path.write_text('{"tags": ["field:CS/AI/CV"]}\n', encoding="utf-8")

    try:
        load_valid_tags_from_file(path=str(path), fmt="json")
        raise AssertionError("expected ValueError for non-array top-level JSON")
    except ValueError as exc:
        assert "top-level list of strings" in str(exc)


def test_validate_valid_tags_auto_ok(tmp_path: Path) -> None:
    path = tmp_path / "valid_tags.yaml"
    path.write_text("- field:CS/AI/CV\n- task:object-detection\n", encoding="utf-8")

    tags, detected_format = load_valid_tags_from_file(path=str(path), fmt="auto")
    assert tags == ["field:CS/AI/CV", "task:object-detection"]
    assert detected_format == "yaml"


def test_validate_valid_tags_auto_rejects_invalid(tmp_path: Path) -> None:
    path = tmp_path / "valid_tags.txt"
    path.write_text("field:CS/AI/CV\ntask:object-detection\n", encoding="utf-8")

    try:
        load_valid_tags_from_file(path=str(path), fmt="auto")
        raise AssertionError("expected ValueError for invalid auto content")
    except ValueError as exc:
        assert "auto detection failed" in str(exc)


def test_validate_valid_tags_main_returns_nonzero_on_invalid(tmp_path: Path) -> None:
    path = tmp_path / "valid_tags.yaml"
    path.write_text("tags:\n  - field:CS/AI/CV\n", encoding="utf-8")

    exit_code = main(["--valid-tags", str(path), "--format", "yaml"])
    assert exit_code == 1
