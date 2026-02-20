## MODIFIED Requirements

### Requirement: Input payload fields
The skill SHALL read a prompt-embedded payload containing `metadata`, `input_tags`, and `infer_tag`, and SHALL read the controlled vocabulary from the Runner input file `input.valid_tags` (file path). The skill SHALL also read:
- `valid_tags_format` with supported values `yaml`, `json`, `auto` (default `yaml`)
- `tag_note_language` as a free-form string used to indicate the language intent for tag meaning notes (recommended BCP 47 naming such as `zh-CN`, `en-US`)

#### Scenario: Payload present with note language
- **WHEN** the prompt contains `metadata`, `input_tags`, optional `infer_tag`, optional `valid_tags_format`, optional `tag_note_language`, and Runner provides a readable `input.valid_tags` file path
- **THEN** the skill treats these as the only source of truth for the run

### Requirement: Required output keys
The output JSON MUST always include the following keys (present even when empty):
- `remove_tags` (array)
- `add_tags` (array)
- `suggest_tags` (array of objects, each object MUST contain `tag` and `note` as strings)
- `provenance.generated_at` (string, UTC ISO-8601)
- `warnings` (array)
- `error` (object|null)

The output JSON MUST also echo back:
- `metadata` (exactly as received)
- `input_tags` (exactly as received)

#### Scenario: Minimal empty output
- **WHEN** no changes are needed and no tags are inferred
- **THEN** the output still contains all required keys, with empty arrays and `error=null`, and includes echoed `metadata` and `input_tags`

## ADDED Requirements

### Requirement: tag_note_language scope isolation
`tag_note_language` MUST only affect the language expression of `suggest_tags[].note`, and MUST NOT affect the values or decision logic of `remove_tags`, `add_tags`, `suggest_tags[].tag`, `warnings`, or `error`.

#### Scenario: Note language only affects note
- **WHEN** `tag_note_language` is provided as `en-US`
- **THEN** `suggest_tags[].note` is expressed in English intent while other output fields keep their original decision behavior
