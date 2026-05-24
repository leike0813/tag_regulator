## MODIFIED Requirements

### Requirement: Inference sources and gating
When inference is enabled, the skill SHALL infer candidate tags using the semantic content of `metadata`, prioritizing (when present) the following fields:
- `title`
- `abstract`
- `keywords`
- `conference_name`
- `publication_title`

If `digest_markdown` is provided and readable, the skill SHALL treat digest content as supplemental evidence after metadata for refining domain/task/method/model understanding and improving `suggest_tags[].note` quality.

If `metadata` is missing or empty, inference MUST be disabled.

#### Scenario: Infer from metadata with digest supplement
- **WHEN** inference is enabled, metadata fields are present, and `digest_markdown` is readable
- **THEN** the skill uses metadata as primary evidence and digest as supplemental evidence

#### Scenario: Digest unavailable but inference enabled
- **WHEN** inference is enabled and `digest_markdown` is missing/unreadable
- **THEN** the skill continues inference using metadata and records a warning only for unreadable digest cases

### Requirement: Inference output routing
For each inferred candidate tag, the skill MUST route outputs as follows:
- If it exists in `valid_tags`, the skill MUST include it in `add_tags` (deduped).
- Otherwise, the skill MUST include an object in `suggest_tags` containing:
  - `tag`: normalized inferred tag
  - `note`: explanation of inferred meaning

Digest evidence MUST NOT bypass controlled vocabulary constraints and MUST NOT be used to directly place out-of-vocabulary tags into `add_tags`.

#### Scenario: Inferred tag out of vocab
- **WHEN** an inferred tag is not present in `valid_tags`
- **THEN** the skill outputs that inferred tag as `suggest_tags[].tag` with a corresponding `suggest_tags[].note`

#### Scenario: Digest suggests out-of-vocabulary concept
- **WHEN** digest evidence indicates a concept not present in `valid_tags`
- **THEN** the skill emits it via `suggest_tags` and does not include it in `add_tags`
