## 1. OpenSpec Artifacts

- [x] 1.1 Create change `optional-valid-tags-pure-inference`.
- [x] 1.2 Add proposal, design, delta specs, and implementation tasks.

## 2. Skill Contract And Assets

- [x] 2.1 Update `tag-regulator/SKILL.md` for optional `valid_tags`, controlled mode, and pure inference mode.
- [x] 2.2 Update `tag-regulator/assets/input.schema.json` so `valid_tags` is optional.
- [x] 2.3 Update `tag-regulator/assets/parameter.schema.json` so `valid_tags_format` only applies when `valid_tags` is provided.
- [x] 2.4 Update `tag-regulator/assets/runner.json` to mark `valid_tags` optional.
- [x] 2.5 Update `README.md` with the new optional valid_tags behavior.

## 3. Validation Tooling

- [x] 3.1 Update `dev-tools/tag-regulator/scripts/validate_output.py` to reject non-empty `add_tags` when no `valid_tags` is available.
- [x] 3.2 Add lightweight structural validation for `suggest_tags[].tag`.
- [x] 3.3 Keep `tag-regulator/scripts/validate_valid_tags.py` strict for explicit file validation.

## 4. Tests And Verification

- [x] 4.1 Add/update tests for optional `valid_tags` input schema and runner prompt.
- [x] 4.2 Add output validator tests for pure inference success, forbidden pure-mode `add_tags`, and invalid suggestion tag structure.
- [x] 4.3 Run `uv run --project="$HOME/.ar" --locked -- python -m pytest -q`.
- [x] 4.4 Run `uv run --project="$HOME/.ar" --locked -- python -m mypy tag-regulator/scripts dev-tools/tag-regulator/scripts`.
