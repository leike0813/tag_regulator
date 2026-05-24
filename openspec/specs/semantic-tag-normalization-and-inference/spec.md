# semantic-tag-normalization-and-inference Specification

## Purpose
TBD - created by archiving change mvp-tag-regulator. Update Purpose after archive.
## Requirements
### Requirement: Controlled vocabulary constraint
The skill MUST treat the parsed contents of `input.valid_tags` as the controlled vocabulary (`valid_tags`), and MUST ensure that every tag in `add_tags` is a member of that parsed `valid_tags` set.

#### Scenario: Add tag in vocabulary
- **WHEN** the skill decides a new tag should be added
- **THEN** it only adds the tag to `add_tags` if it exists in the parsed `valid_tags`

### Requirement: Suggest out-of-vocabulary tags
If the skill identifies a semantically relevant tag that is not present in `valid_tags`, it MUST NOT add it to `add_tags` and MUST instead place it into `suggest_tags` after normalizing it to the tag naming standard.  
Each suggestion entry in `suggest_tags` MUST be an object with:
- `tag` (normalized candidate tag string)
- `note` (natural-language explanation of the tag meaning inferred by the agent)

#### Scenario: Candidate not in valid_tags
- **WHEN** the skill identifies a relevant tag that is not in `valid_tags`
- **THEN** it emits an object `{ "tag": "<normalized-tag>", "note": "<semantic explanation>" }` in `suggest_tags` and does not include that tag in `add_tags`

### Requirement: Semantic normalization of input_tags
The skill SHALL semantically normalize `input_tags` by mapping each input tag to one of:
- a canonical tag in `valid_tags` (preferred)
- an out-of-vocabulary canonical candidate (emitted to `suggest_tags`)
- removal (emit the original input tag in `remove_tags` when it should be removed)

Normalization MUST be based on semantic understanding, not only exact string matching, and MUST follow the naming standard described by the project references (facet conventions, case rules, and path formatting).

#### Scenario: Synonym mapping
- **WHEN** an `input_tag` is a synonym/paraphrase of a valid controlled tag
- **THEN** the skill removes the original `input_tag` (include it in `remove_tags`) and adds the controlled tag to `add_tags`

### Requirement: remove_tags constraints
Every element of `remove_tags` MUST be an element from the received `input_tags` (original strings). The skill MUST NOT invent new strings in `remove_tags`.

#### Scenario: Remove tag is from input
- **WHEN** the skill outputs `remove_tags`
- **THEN** each removed tag is present in `input_tags`

### Requirement: add_tags uniqueness
`add_tags` MUST NOT contain duplicate elements.

#### Scenario: Duplicate prevention
- **WHEN** multiple inputs/inference paths produce the same controlled tag
- **THEN** the skill includes that tag only once in `add_tags`

### Requirement: suggest_tags uniqueness
`suggest_tags` MUST NOT contain duplicate suggestion tags. The uniqueness key MUST be `suggest_tags[].tag`.

#### Scenario: Duplicate suggestion prevention
- **WHEN** multiple reasoning paths produce the same suggested tag with different notes
- **THEN** the skill includes that suggested tag only once in `suggest_tags`

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

### Requirement: Warnings for low-confidence outputs
When the skill is uncertain about a normalization or inference decision, it MUST include an entry in `warnings` describing the uncertainty (without violating JSON-only stdout).

#### Scenario: Uncertain inference
- **WHEN** inference yields multiple plausible tags with low confidence
- **THEN** the skill uses a conservative output and appends a warning describing the uncertainty

### Requirement: Stable, machine-friendly ordering
The skill SHALL produce stable outputs suitable for batch automation:
- `remove_tags` SHOULD preserve the order of the removed tags as they appear in `input_tags`.
- `add_tags` MUST be output in a stable order (deterministic for the same input payload).
- `suggest_tags` MUST be output in a stable order by `suggest_tags[].tag` (deterministic for the same input payload).

#### Scenario: Repeatable run
- **WHEN** the skill is run multiple times with the same payload
- **THEN** it produces identical ordering for `remove_tags`, `add_tags`, and `suggest_tags`

### Requirement: Suggestion note language control
When `tag_note_language` is provided, the skill MUST express `suggest_tags[].note` in the requested language intent, while preserving the semantic meaning of `suggest_tags[].tag`.

#### Scenario: Chinese note output
- **WHEN** `tag_note_language=zh-CN` and the skill produces suggestion notes
- **THEN** each `suggest_tags[].note` is expressed in Chinese intent for the same suggested tag meaning

