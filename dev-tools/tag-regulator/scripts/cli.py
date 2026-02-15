from __future__ import annotations

import argparse
import os
import sys


THIS_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(THIS_DIR, "..", "..", ".."))
RUNTIME_SCRIPTS = os.path.join(REPO_ROOT, "tag-regulator", "scripts")

if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)
if RUNTIME_SCRIPTS not in sys.path:
    sys.path.insert(0, RUNTIME_SCRIPTS)

from normalize_output import main as normalize_main  # type: ignore  # noqa: E402
from validate_output import main as validate_main  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="tag-regulator-cli", description="Local dev utilities for tag-regulator.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="Validate a captured output JSON.")
    v.add_argument("--output", required=True)
    v.add_argument("--payload")
    v.add_argument("--schema")

    n = sub.add_parser("normalize", help="Normalize a captured output JSON in-place.")
    n.add_argument("--output", required=True)

    args = parser.parse_args(argv)

    if args.cmd == "validate":
        validate_argv: list[str] = ["--output", args.output]
        if args.payload:
            validate_argv += ["--payload", args.payload]
        if args.schema:
            validate_argv += ["--schema", args.schema]
        return validate_main(validate_argv)

    if args.cmd == "normalize":
        return normalize_main(["--output", args.output])

    raise AssertionError(f"Unhandled command: {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
