## MODIFIED Requirements

### Requirement: Input payload fields
The skill SHALL read a prompt-embedded payload containing optional `metadata`, optional `input_tags`, and optional `infer_tag`. The Runner input files `input.valid_tags` and `input.digest_markdown` SHALL be optional.

If `input_tags` is missing, the skill MUST treat it as an empty string array for processing and output echoing.

#### Scenario: Missing input_tags
- **WHEN** the prompt does not contain `input_tags`
- **THEN** the skill treats `input_tags` as `[]` and still includes `"input_tags": []` in output

### Requirement: Default infer_tag behavior
The skill MUST determine effective tag inference according to available evidence and mode:

1) In controlled vocabulary mode, `input_tags` normalization MUST still run when `input_tags` exist, regardless of `infer_tag`.
2) In controlled vocabulary mode, explicit `infer_tag=false` MUST disable metadata/digest-driven additional inference.
3) In controlled vocabulary mode, if `infer_tag` is missing or cannot be interpreted and metadata or readable digest evidence exists, inference defaults to enabled.
4) In pure inference mode, `infer_tag=false` MUST NOT disable inference from available `input_tags`, metadata, or readable digest evidence.
5) If no usable evidence exists, the skill MUST return an `insufficient_input` error.

#### Scenario: Digest-only inference evidence
- **WHEN** `metadata` is missing or empty, readable non-empty `digest_markdown` is provided, and inference is otherwise enabled
- **THEN** the skill may infer tags from digest evidence

#### Scenario: Controlled mode explicit false
- **WHEN** `valid_tags` is provided and `infer_tag=false`
- **THEN** the skill still normalizes existing `input_tags` but does not add metadata/digest-only inferred tags

#### Scenario: Pure inference explicit false
- **WHEN** `valid_tags` is absent, `infer_tag=false`, and any usable evidence exists
- **THEN** the skill still produces pure inference `suggest_tags` when relevant

## ADDED Requirements

### Requirement: Insufficient input failure
If `metadata`, readable non-empty `digest_markdown`, `input_tags`, and `valid_tags` are all absent or empty, the skill MUST return schema-compatible output with:
- `input_tags=[]`
- `remove_tags=[]`
- `add_tags=[]`
- `suggest_tags=[]`
- `error.type="insufficient_input"`

#### Scenario: No usable inputs
- **WHEN** the payload provides no metadata, no input tags, no valid_tags, and no readable non-empty digest markdown
- **THEN** the skill returns an `insufficient_input` error JSON and does not attempt semantic inference
