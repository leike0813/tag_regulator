# semantic-tag-normalization-and-inference Specification

## Purpose
TBD - created by archiving change mvp-tag-regulator. Update Purpose after archive.
## Requirements
### Requirement: Controlled vocabulary constraint
When `input.valid_tags` is provided, the skill MUST treat its parsed contents as the controlled vocabulary and MUST ensure that every tag in `add_tags` is a member of that parsed set.

When `input.valid_tags` is absent, the skill MUST NOT emit any `add_tags`.

#### Scenario: Add tag in vocabulary
- **WHEN** the skill runs with `valid_tags` and decides a new tag should be added
- **THEN** it only adds the tag to `add_tags` if it exists in the parsed `valid_tags`

#### Scenario: No vocabulary means no additions
- **WHEN** the skill runs without `valid_tags`
- **THEN** `add_tags` is empty even if the skill identifies relevant normalized candidates

### Requirement: Suggest out-of-vocabulary tags
If the skill identifies a semantically relevant tag that is not present in `valid_tags`, or if no `valid_tags` set exists, it MUST NOT add it to `add_tags` and MUST instead place it into `suggest_tags` after normalizing it to the tag naming standard.

Each suggestion entry in `suggest_tags` MUST be an object with:
- `tag` (normalized candidate tag string)
- `note` (natural-language explanation of the tag meaning inferred by the agent)

#### Scenario: Candidate not in valid_tags
- **WHEN** the skill identifies a relevant tag that is not in the provided `valid_tags`
- **THEN** it emits an object `{ "tag": "<normalized-tag>", "note": "<semantic explanation>" }` in `suggest_tags` and does not include that tag in `add_tags`

#### Scenario: Candidate without valid_tags
- **WHEN** the skill identifies a relevant tag while running without `valid_tags`
- **THEN** it emits that candidate in `suggest_tags` and leaves `add_tags` empty

### Requirement: Semantic normalization of input_tags
When `valid_tags` is provided, the skill SHALL semantically normalize `input_tags` by mapping each input tag to one of:
- a canonical tag in `valid_tags` (preferred)
- an out-of-vocabulary canonical candidate (emitted to `suggest_tags`)
- removal (emit the original input tag in `remove_tags` when it should be removed)

When `valid_tags` is absent, the skill SHALL treat `input_tags` as evidence for pure inference and MUST NOT emit removals based on them.

#### Scenario: Pure inference keeps input_tags unchanged
- **WHEN** an `input_tag` can be normalized but no `valid_tags` was provided
- **THEN** the normalized candidate is emitted in `suggest_tags` and the original `input_tag` is not emitted in `remove_tags`

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

### Requirement: Inference output routing
For each inferred candidate tag, the skill MUST route outputs as follows:
- If `valid_tags` exists and the candidate exists in it, include it in `add_tags`.
- Otherwise, include an object in `suggest_tags`.

Digest evidence MUST NOT bypass controlled vocabulary constraints and MUST NOT place tags into `add_tags` when no vocabulary exists.

#### Scenario: Inferred tag out of vocab
- **WHEN** an inferred tag is not present in provided `valid_tags`
- **THEN** the skill outputs that inferred tag as `suggest_tags[].tag`

#### Scenario: Inferred tag without vocab
- **WHEN** inference is enabled and `valid_tags` is absent
- **THEN** inferred candidates are emitted through `suggest_tags` only

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

