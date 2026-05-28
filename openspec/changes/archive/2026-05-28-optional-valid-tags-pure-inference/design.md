## Context

The skill has two distinct use cases:

- Controlled vocabulary mode: a caller provides `valid_tags`, and the skill can safely produce writeback actions through `remove_tags` and `add_tags`.
- Pure inference mode: a caller has no controlled vocabulary and only wants normalized candidate tags for review.

The output schema remains stable in both modes so downstream callers do not need a new response type.

## Decisions

### Optional `valid_tags` Selects Mode

The presence of `input.valid_tags` selects controlled vocabulary mode. If it is missing or empty, the skill enters pure inference mode.

In controlled vocabulary mode:

- `validate_valid_tags.py` is called before semantic work.
- `valid_tags_format` is honored exactly as before.
- `add_tags` must be a subset of the parsed vocabulary.
- `suggest_tags[].tag` must not be present in the parsed vocabulary.

In pure inference mode:

- `validate_valid_tags.py` is not called.
- `valid_tags_format` has no effect.
- `remove_tags` remains empty to avoid destructive cleanup without a trusted target vocabulary.
- `add_tags` remains empty because there is no controlled vocabulary.
- Candidates from `input_tags`, `metadata`, and readable `digest_markdown` are normalized into `suggest_tags`.

### Suggestion Structure Validation

The development output validator will enforce stable structural rules for `suggest_tags[].tag`: one colon, known lowercase facet, non-empty path/value, no whitespace, and no empty path segments. It will not try to validate semantics or a full abbreviation registry because that would reject legitimate future vocabulary expansion.

### Existing Script Boundaries

`tag-regulator/scripts/validate_valid_tags.py` remains a strict validator for an explicit file path. Optionality is handled by the skill flow and schemas, not by making the script silently accept missing input.

## Risks

- Pure inference outputs could be mistaken for writeback actions if a caller ignores field semantics. This is mitigated by forcing `remove_tags=[]` and `add_tags=[]` when `valid_tags` is absent.
- Lightweight tag validation cannot prove semantic correctness. This is acceptable because the skill's semantic step remains LLM-driven and `suggest_tags` are advisory.
