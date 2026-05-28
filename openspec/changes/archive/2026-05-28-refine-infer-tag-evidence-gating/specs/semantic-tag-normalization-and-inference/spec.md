## MODIFIED Requirements

### Requirement: Inference sources and gating
When inference is enabled or pure inference mode is active, the skill SHALL infer candidate tags using available semantic evidence from:
- `input_tags`
- `metadata`
- readable non-empty `digest_markdown`

If `metadata` is missing but readable non-empty `digest_markdown` exists, inference MUST NOT be disabled solely because metadata is missing.

#### Scenario: Digest substitutes for metadata
- **WHEN** metadata is missing and digest markdown is readable and non-empty
- **THEN** digest content may drive tag inference

#### Scenario: No digest evidence
- **WHEN** digest markdown is missing, empty, or unreadable
- **THEN** digest contributes no inference evidence; unreadable digest is ignored with a warning

## ADDED Requirements

### Requirement: Pure inference cannot be no-op when evidence exists
When `valid_tags` is absent and at least one evidence source is available, the skill MUST treat pure inference as active even if the user provided `infer_tag=false`.

#### Scenario: Pure inference with false infer_tag
- **WHEN** `valid_tags` is absent, `infer_tag=false`, and input tag or metadata or digest evidence exists
- **THEN** the skill emits relevant normalized candidates through `suggest_tags` and keeps `remove_tags=[]` and `add_tags=[]`

### Requirement: Controlled mode input normalization independent from infer_tag
When `valid_tags` is provided, `infer_tag=false` MUST NOT disable semantic normalization of existing `input_tags`.

#### Scenario: Controlled normalization with false infer_tag
- **WHEN** `valid_tags` is provided, `infer_tag=false`, and an `input_tag` maps to a controlled tag
- **THEN** the skill may emit the original tag in `remove_tags` and the controlled tag in `add_tags`
