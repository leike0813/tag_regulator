## 1. OpenSpec Artifacts

- [x] 1.1 Create change `refine-infer-tag-evidence-gating`.
- [x] 1.2 Add proposal, design, delta specs, and implementation tasks.

## 2. Skill Contract And Assets

- [x] 2.1 Update `tag-regulator/SKILL.md` for revised evidence gating and insufficient-input behavior.
- [x] 2.2 Update `tag-regulator/assets/input.schema.json` so `input_tags` is optional.
- [x] 2.3 Update `tag-regulator/assets/parameter.schema.json` so `infer_tag` describes controlled-mode and pure-mode behavior.
- [x] 2.4 Update `tag-regulator/assets/runner.json` and `README.md` with the new input/evidence rules.

## 3. Validation Tooling

- [x] 3.1 Update `dev-tools/tag-regulator/scripts/validate_output.py` to accept missing payload `input_tags` as `[]`.
- [x] 3.2 Add output validation coverage for `insufficient_input`.
- [x] 3.3 Leave `normalize_output.py` and `validate_valid_tags.py` unchanged.

## 4. Tests And Verification

- [x] 4.1 Add/update schema and skill contract tests for optional `input_tags` and revised `infer_tag` docs.
- [x] 4.2 Add validator tests for digest-only inference, pure inference with `infer_tag=false`, insufficient input, and controlled input normalization with `infer_tag=false`.
- [x] 4.3 Run `uv run --project="$HOME/.ar" --locked -- python -m pytest -q`.
- [x] 4.4 Run `uv run --project="$HOME/.ar" --locked -- python -m mypy tag-regulator/scripts dev-tools/tag-regulator/scripts`.
- [x] 4.5 Run `openspec validate refine-infer-tag-evidence-gating`.
