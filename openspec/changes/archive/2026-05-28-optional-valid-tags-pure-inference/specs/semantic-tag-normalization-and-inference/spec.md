## MODIFIED Requirements

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
