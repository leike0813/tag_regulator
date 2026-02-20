## MODIFIED Requirements

### Requirement: Suggest out-of-vocabulary tags
If the skill identifies a semantically relevant tag that is not present in `valid_tags`, it MUST NOT add it to `add_tags` and MUST instead place it into `suggest_tags` after normalizing it to the tag naming standard.  
Each suggestion entry in `suggest_tags` MUST be an object with:
- `tag` (normalized candidate tag string)
- `note` (natural-language explanation of the tag meaning inferred by the agent)

#### Scenario: Candidate not in valid_tags
- **WHEN** the skill identifies a relevant tag that is not in `valid_tags`
- **THEN** it emits an object `{ "tag": "<normalized-tag>", "note": "<semantic explanation>" }` in `suggest_tags` and does not include that tag in `add_tags`

### Requirement: suggest_tags uniqueness
`suggest_tags` MUST NOT contain duplicate suggestion tags. The uniqueness key MUST be `suggest_tags[].tag`.

#### Scenario: Duplicate suggestion prevention
- **WHEN** multiple reasoning paths produce the same suggested tag with different notes
- **THEN** the skill includes that suggested tag only once in `suggest_tags`

### Requirement: Inference output routing
For each inferred candidate tag, the skill MUST route outputs as follows:
- If it exists in `valid_tags`, the skill MUST include it in `add_tags` (deduped).
- Otherwise, the skill MUST include an object in `suggest_tags` containing:
  - `tag`: normalized inferred tag
  - `note`: explanation of inferred meaning

#### Scenario: Inferred tag out of vocab
- **WHEN** an inferred tag is not present in `valid_tags`
- **THEN** the skill outputs that inferred tag as `suggest_tags[].tag` with a corresponding `suggest_tags[].note`

### Requirement: Stable, machine-friendly ordering
The skill SHALL produce stable outputs suitable for batch automation:
- `remove_tags` SHOULD preserve the order of the removed tags as they appear in `input_tags`.
- `add_tags` MUST be output in a stable order (deterministic for the same input payload).
- `suggest_tags` MUST be output in a stable order by `suggest_tags[].tag` (deterministic for the same input payload).

#### Scenario: Repeatable run
- **WHEN** the skill is run multiple times with the same payload
- **THEN** it produces identical ordering for `remove_tags`, `add_tags`, and `suggest_tags`

## ADDED Requirements

### Requirement: Suggestion note language control
When `tag_note_language` is provided, the skill MUST express `suggest_tags[].note` in the requested language intent, while preserving the semantic meaning of `suggest_tags[].tag`.

#### Scenario: Chinese note output
- **WHEN** `tag_note_language=zh-CN` and the skill produces suggestion notes
- **THEN** each `suggest_tags[].note` is expressed in Chinese intent for the same suggested tag meaning
