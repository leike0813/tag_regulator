## Context

The current effective `infer_tag` rule predates two later capabilities:

- `digest_markdown` can provide semantic evidence even when `metadata` is absent.
- Missing `valid_tags` selects pure inference mode, where suggestions are the only useful output.

The skill should distinguish two concepts:

- Whether metadata/digest-driven inference should be suppressed in controlled vocabulary mode.
- Whether the run has enough evidence to produce any meaningful output.

## Decisions

### Evidence Sources

Usable evidence consists of:

- non-empty `input_tags`
- non-empty `metadata`
- readable and non-empty `digest_markdown`
- valid `valid_tags` for controlled vocabulary mode

Unreadable `digest_markdown` remains non-fatal and is ignored after recording a warning.

### Effective `infer_tag`

Controlled vocabulary mode:

- `input_tags` normalization always runs when `input_tags` exist.
- `infer_tag=false` disables metadata/digest-driven additional inference.
- If `infer_tag` is missing or unparseable, use the existing default-to-true behavior when metadata or digest evidence exists.

Pure inference mode:

- There are no writeback actions, so `input_tags`, metadata, and readable digest are all suggestion evidence.
- `infer_tag=false` does not disable pure inference; otherwise a no-vocabulary run with evidence would be a no-op.
- The skill may add a warning when it overrides `infer_tag=false` in pure inference mode.

### Insufficient Input

When `metadata`, readable `digest_markdown`, `input_tags`, and `valid_tags` are all absent or empty, the skill returns a schema-compatible error JSON with:

- `input_tags=[]`
- `remove_tags=[]`
- `add_tags=[]`
- `suggest_tags=[]`
- `error.type="insufficient_input"`

This preserves the stdout single-JSON contract.

## Risks

- Overriding `infer_tag=false` in pure inference mode is a semantic change. It is limited to no-vocabulary runs, where suggestions are the only useful behavior.
- Making `input_tags` optional changes input schema expectations. The skill keeps `input_tags=[]` in output when absent to preserve the required output key.
