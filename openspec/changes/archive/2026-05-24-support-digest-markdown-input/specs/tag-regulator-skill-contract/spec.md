## MODIFIED Requirements

### Requirement: Input payload fields
The skill SHALL read a prompt-embedded payload containing `metadata`, `input_tags`, and `infer_tag`, and SHALL read the controlled vocabulary from the Runner input file `input.valid_tags` (file path). The skill SHALL also read:
- `valid_tags_format` with supported values `yaml`, `json`, `auto` (default `yaml`)
- `tag_note_language` as a free-form string used to indicate the language intent for tag meaning notes (recommended BCP 47 naming such as `zh-CN`, `en-US`)
- `digest_markdown` as an optional Markdown file path containing paper digest context

#### Scenario: Payload present with note language and digest path
- **WHEN** the prompt contains `metadata`, `input_tags`, optional `infer_tag`, optional `valid_tags_format`, optional `tag_note_language`, optional `digest_markdown`, and Runner provides a readable `input.valid_tags` file path
- **THEN** the skill treats these as the only source of truth for the run

## ADDED Requirements

### Requirement: Optional digest_markdown is non-fatal
`digest_markdown` input MUST be treated as optional enhancement context. If it is missing, empty, unreadable, or has encoding errors, the skill MUST continue execution without failing the run.

#### Scenario: Missing digest_markdown
- **WHEN** `digest_markdown` is not provided
- **THEN** the skill continues normal processing using existing evidence sources and does not return error

#### Scenario: Unreadable digest_markdown
- **WHEN** `digest_markdown` is provided but file reading fails due to permissions/path/encoding issues
- **THEN** the skill appends a warning and ignores digest context while continuing the run
