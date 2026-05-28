## Why

`$tag-regulator` currently requires a controlled vocabulary file for every run, which makes the skill hard to reuse when a caller only wants normalized tag suggestions. Supporting an optional `valid_tags` input lets the same skill operate either as a strict writeback regulator or as a pure inference assistant.

## What Changes

- Make `input.valid_tags` optional instead of required.
- Add pure inference mode for runs without `valid_tags`: keep `remove_tags=[]` and `add_tags=[]`, and route every normalized candidate to `suggest_tags`.
- Keep controlled vocabulary mode unchanged when `valid_tags` is provided: validate the file first, require `add_tags` to be in the parsed vocabulary, and keep vocabulary members out of `suggest_tags`.
- Add lightweight output validation for `suggest_tags[].tag` structure so pure inference still follows the tag naming standard.
- Update skill docs, runner/input schemas, README, validation tooling, and tests.

## Capabilities

### New Capabilities

### Modified Capabilities

- `tag-regulator-skill-contract`: `input.valid_tags` becomes optional, and missing `valid_tags` selects pure inference instead of error output.
- `semantic-tag-normalization-and-inference`: inference and normalization gain a no-vocabulary routing mode that only emits `suggest_tags`.
- `skill-script-invocation-contract`: the `valid_tags` validation script is called only when a `valid_tags` file is provided.

## Impact

- Affected published skill files: `tag-regulator/SKILL.md`, `tag-regulator/assets/input.schema.json`, `tag-regulator/assets/parameter.schema.json`, `tag-regulator/assets/runner.json`.
- Affected development tooling: `dev-tools/tag-regulator/scripts/validate_output.py`.
- Tests are extended under `tests/`; no dependency changes are required.
