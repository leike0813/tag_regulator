## Why

`infer_tag` still uses the original metadata-only boundary even though `digest_markdown` can now supply inference evidence and `valid_tags` can be omitted for pure inference. This can incorrectly disable useful inference or turn pure inference runs into no-ops.

## What Changes

- Refine `infer_tag` gating to consider available evidence from `metadata`, readable `digest_markdown`, and `input_tags`.
- Make `input_tags` optional; missing or empty `input_tags` is treated as no input-tag evidence.
- In pure inference mode, do not let `infer_tag=false` disable all inference when evidence exists.
- Add an `insufficient_input` error output when no usable evidence exists and no `valid_tags` was provided.
- Update skill docs, schemas, runner prompt, README, validation tooling, and tests.

## Capabilities

### New Capabilities

### Modified Capabilities

- `tag-regulator-skill-contract`: refine input optionality, insufficient-input failure, and `infer_tag` effective behavior.
- `semantic-tag-normalization-and-inference`: refine inference evidence sources and pure-mode inference routing.

## Impact

- Affected published skill files: `tag-regulator/SKILL.md`, `tag-regulator/assets/input.schema.json`, `tag-regulator/assets/parameter.schema.json`, `tag-regulator/assets/runner.json`.
- Affected development tooling: `dev-tools/tag-regulator/scripts/validate_output.py`.
- Tests are extended under `tests/`; no dependency changes are required.
