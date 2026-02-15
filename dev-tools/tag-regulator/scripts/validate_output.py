from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from typing import Any, Iterable

from jsonschema import Draft7Validator
import yaml


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_valid_tags_from_file(*, path: str, fmt: str) -> list[str]:
    content = _load_text(path)

    def parse_yaml_list(text: str) -> list[str]:
        obj = yaml.safe_load(text)
        if not isinstance(obj, list) or not all(isinstance(x, str) for x in obj):
            raise ValueError("yaml content must be a top-level list of strings")
        return obj

    def parse_json_list(text: str) -> list[str]:
        obj = json.loads(text)
        if not isinstance(obj, list) or not all(isinstance(x, str) for x in obj):
            raise ValueError("json content must be a top-level list of strings")
        return obj

    if fmt == "yaml":
        return parse_yaml_list(content)
    if fmt == "json":
        return parse_json_list(content)
    if fmt == "auto":
        for candidate in ("yaml", "json"):
            try:
                return load_valid_tags_from_file(path=path, fmt=candidate)
            except Exception:
                continue
        raise ValueError("auto detection failed to parse as yaml/json list of strings")
    raise ValueError(f"unsupported valid_tags_format: {fmt!r}")


def _dedup_check(values: Iterable[str]) -> bool:
    seen: set[str] = set()
    for v in values:
        if v in seen:
            return False
        seen.add(v)
    return True


def validate_output_data(
    *,
    output_data: Any,
    schema_data: Any,
    payload_data: Any | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    validator = Draft7Validator(schema_data)
    for err in sorted(validator.iter_errors(output_data), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in err.path) or "$"
        issues.append(ValidationIssue(path=path, message=err.message))

    if not isinstance(output_data, dict):
        issues.append(ValidationIssue(path="$", message="output must be a JSON object"))
        return issues

    input_tags = output_data.get("input_tags", None)
    remove_tags = output_data.get("remove_tags", None)
    add_tags = output_data.get("add_tags", None)
    suggest_tags = output_data.get("suggest_tags", None)

    if isinstance(add_tags, list) and all(isinstance(x, str) for x in add_tags):
        if not _dedup_check(add_tags):
            issues.append(ValidationIssue(path="add_tags", message="add_tags must not contain duplicates"))

    if isinstance(suggest_tags, list) and all(isinstance(x, str) for x in suggest_tags):
        if not _dedup_check(suggest_tags):
            issues.append(
                ValidationIssue(path="suggest_tags", message="suggest_tags must not contain duplicates")
            )

    if isinstance(remove_tags, list) and all(isinstance(x, str) for x in remove_tags):
        if not _dedup_check(remove_tags):
            issues.append(ValidationIssue(path="remove_tags", message="remove_tags must not contain duplicates"))

    if (
        isinstance(input_tags, list)
        and all(isinstance(x, str) for x in input_tags)
        and isinstance(remove_tags, list)
        and all(isinstance(x, str) for x in remove_tags)
    ):
        input_set = set(input_tags)
        for t in remove_tags:
            if t not in input_set:
                issues.append(
                    ValidationIssue(path="remove_tags", message=f"remove tag not present in input_tags: {t!r}")
                )

    if payload_data is not None and isinstance(payload_data, dict):
        payload_input_tags = payload_data.get("input_tags", None)
        payload_valid_tags = payload_data.get("valid_tags", None)

        if isinstance(payload_input_tags, list) and all(isinstance(x, str) for x in payload_input_tags):
            if isinstance(input_tags, list) and input_tags != payload_input_tags:
                issues.append(
                    ValidationIssue(path="input_tags", message="output input_tags does not match payload input_tags")
                )

        if isinstance(payload_valid_tags, list) and all(isinstance(x, str) for x in payload_valid_tags):
            valid_set = set(payload_valid_tags)
            if isinstance(add_tags, list) and all(isinstance(x, str) for x in add_tags):
                for t in add_tags:
                    if t not in valid_set:
                        issues.append(
                            ValidationIssue(path="add_tags", message=f"add tag not present in valid_tags: {t!r}")
                        )
            if isinstance(suggest_tags, list) and all(isinstance(x, str) for x in suggest_tags):
                for t in suggest_tags:
                    if t in valid_set:
                        issues.append(
                            ValidationIssue(
                                path="suggest_tags",
                                message=f"suggest tag MUST NOT be in valid_tags (should be added instead): {t!r}",
                            )
                        )

    return issues


def validate_files(*, output_path: str, payload_path: str | None = None, schema_path: str) -> list[ValidationIssue]:
    output_data = _load_json(output_path)
    schema_data = _load_json(schema_path)
    payload_data = _load_json(payload_path) if payload_path else None
    return validate_output_data(output_data=output_data, schema_data=schema_data, payload_data=payload_data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate tag-regulator output JSON.")
    parser.add_argument("--output", required=True, help="Path to the output JSON to validate.")
    parser.add_argument("--payload", help="Optional payload JSON containing valid_tags/input_tags for constraint checks.")
    parser.add_argument(
        "--valid-tags-file",
        help="Optional valid tags file for constraint checks when payload does not include valid_tags.",
    )
    parser.add_argument(
        "--valid-tags-format",
        default="yaml",
        choices=["yaml", "json", "auto"],
        help="Format of --valid-tags-file (default: yaml).",
    )
    parser.add_argument(
        "--schema",
        default=os.path.join(os.path.dirname(__file__), "..", "assets", "output_schema.json"),
        help="Path to JSON Schema for the output.",
    )
    args = parser.parse_args(argv)

    payload_data = _load_json(args.payload) if args.payload else None
    if args.valid_tags_file:
        valid_tags = load_valid_tags_from_file(path=args.valid_tags_file, fmt=args.valid_tags_format)
        if payload_data is None or not isinstance(payload_data, dict):
            payload_data = {}
        payload_data = dict(payload_data)
        payload_data["valid_tags"] = valid_tags

    output_data = _load_json(args.output)
    schema_data = _load_json(args.schema)
    issues = validate_output_data(output_data=output_data, schema_data=schema_data, payload_data=payload_data)
    if issues:
        for issue in issues:
            print(f"{issue.path}: {issue.message}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
