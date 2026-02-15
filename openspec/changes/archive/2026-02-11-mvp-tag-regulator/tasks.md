## 1. Skill package skeleton

- [x] 1.1 Create publish directory `tag-regulator/` skeleton (SKILL.md, optional scripts/assets folders)
- [x] 1.2 Add a minimal `tag-regulator/README.md` clarifying publish boundary (what ships vs dev-only)

## 2. Core Agent Skill instructions (SKILL.md)

- [x] 2.1 Write `tag-regulator/SKILL.md` frontmatter (name/description/compatibility) aligned with `$tag-regulator` usage
- [x] 2.2 Document the strict runtime contract (non-interactive, JSON-only stdout, required keys, echo `metadata` + `input_tags`)
- [x] 2.3 Encode the decision procedure for semantic normalization under `valid_tags` constraint (map/remove/suggest)
- [x] 2.4 Encode inference procedure gated by `infer_tag` + metadata presence (field priority, conservative defaults, routing to add vs suggest)
- [x] 2.5 Define output shaping rules: deduplication and stable ordering for `remove_tags`/`add_tags`/`suggest_tags`
- [x] 2.6 Add at least 3 anchored examples in SKILL.md (payload → exact JSON output) covering: no-op, synonym normalization, inference+suggest
- [x] 2.7 Add explicit failure-mode examples (missing/invalid `valid_tags`, missing metadata disables inference) with `error` populated

## 3. Auxiliary validation/normalization scripts (optional but recommended)

- [x] 3.1 Add `tag-regulator/assets/output_schema.json` capturing the required output shape (including `metadata` and `input_tags`)
- [x] 3.2 Implement `tag-regulator/scripts/validate_output.py` to validate schema and constraints (`add_tags ⊆ valid_tags`, `remove_tags ⊆ input_tags`, no duplicates)
- [x] 3.3 Implement `tag-regulator/scripts/normalize_output.py` to apply stable ordering + dedup (without changing echoed `metadata`/`input_tags`)
- [x] 3.4 Add a small CLI entrypoint for local checks (e.g., validate a saved JSON output file) without emitting non-JSON stdout in skill runtime

## 4. Tests and type checking

- [x] 4.1 Add minimal fixtures for payload + expected output cases (including error cases)
- [x] 4.2 Add unit tests for validation/normalization scripts (pytest) using fixtures
- [x] 4.3 Add mypy configuration and type-check the Python scripts in `tag-regulator/scripts/`
- [x] 4.4 Add a single `conda run --no-capture-output -n DataProcessing ...` command snippet to run tests + mypy locally

## 5. Packaging hygiene

- [x] 5.1 Confirm `tag-regulator/` contains only publishable artifacts (no dev caches, no unrelated files)
- [x] 5.2 Add a lightweight “release checklist” section to `tag-regulator/README.md` (what to verify before publishing)
