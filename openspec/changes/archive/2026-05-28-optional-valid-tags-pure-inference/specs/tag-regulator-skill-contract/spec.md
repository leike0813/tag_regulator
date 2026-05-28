## MODIFIED Requirements

### Requirement: Input payload fields
The skill SHALL read a prompt-embedded payload containing `metadata`, `input_tags`, and `infer_tag`. The Runner input file `input.valid_tags` SHALL be optional. The skill SHALL also read:
- `valid_tags_format` with supported values `yaml`, `json`, `auto` (default `yaml`), used only when `input.valid_tags` is provided
- `tag_note_language` as a free-form string used to indicate the language intent for tag meaning notes
- `digest_markdown` as an optional Markdown file path containing paper digest context

#### Scenario: Payload present with valid_tags
- **WHEN** the prompt contains `metadata`, `input_tags`, optional `infer_tag`, optional `valid_tags_format`, optional `tag_note_language`, optional `digest_markdown`, and Runner provides a readable `input.valid_tags` file path
- **THEN** the skill uses controlled vocabulary mode and treats the parsed `valid_tags` as the only source of truth for `add_tags`

#### Scenario: Payload present without valid_tags
- **WHEN** the prompt contains `metadata`, `input_tags`, optional `infer_tag`, optional `tag_note_language`, optional `digest_markdown`, and Runner does not provide `input.valid_tags`
- **THEN** the skill uses pure inference mode and does not return an error solely because `valid_tags` is missing

### Requirement: Failure handling for missing input_tags or valid_tags
If reading `input_tags` fails, OR if `input.valid_tags` is provided but reading/parsing/validating it fails (unreadable/invalid type/encoding/format/content shape error), the skill MUST return schema-compatible output with:
- `remove_tags=[]`
- `add_tags=[]`
- `error` set to a non-null object describing the failure

Missing `input.valid_tags` MUST NOT trigger this failure handling.

#### Scenario: valid_tags missing
- **WHEN** `input.valid_tags` is not provided
- **THEN** the skill continues in pure inference mode with `error=null`

#### Scenario: valid_tags content shape invalid
- **WHEN** `input.valid_tags` is provided and can be read but parsed result is not a top-level list of strings
- **THEN** the skill returns schema-compatible output with empty `remove_tags` and `add_tags` and a non-null `error` object

## ADDED Requirements

### Requirement: Pure inference output shape
When `input.valid_tags` is absent, the output JSON MUST still include all required keys and MUST set:
- `remove_tags=[]`
- `add_tags=[]`

The skill MAY include normalized candidates in `suggest_tags`.

#### Scenario: Pure inference suggestions
- **WHEN** the skill runs without `input.valid_tags` and identifies relevant normalized tag candidates
- **THEN** it emits those candidates in `suggest_tags`, keeps `remove_tags=[]` and `add_tags=[]`, and sets `error=null`
