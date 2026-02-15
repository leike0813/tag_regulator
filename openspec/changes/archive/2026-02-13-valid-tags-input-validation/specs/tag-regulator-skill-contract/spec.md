## MODIFIED Requirements

### Requirement: Input payload fields
The skill SHALL read a prompt-embedded payload containing `metadata`, `input_tags`, and `infer_tag`, and SHALL read the controlled vocabulary from the Runner input file `input.valid_tags` (file path). The skill SHALL also read `valid_tags_format` with supported values `yaml`, `json`, `auto` (default `yaml`).

#### Scenario: Payload present and valid_tags file present
- **WHEN** the prompt contains `metadata`, `input_tags`, optional `infer_tag`, and optional `valid_tags_format`, and Runner provides a readable `input.valid_tags` file path
- **THEN** the skill treats these as the only source of truth for the run

### Requirement: Failure handling for missing input_tags or valid_tags
If reading `input_tags` fails OR reading/parsing/validating `input.valid_tags` fails (missing/unreadable/invalid type/encoding/format/content shape error), the skill MUST return schema-compatible output with:
- `remove_tags=[]`
- `add_tags=[]`
- `error` set to a non-null object describing the failure

`warnings` MUST still be present (may be empty), `provenance.generated_at` MUST still be present, and `metadata`/`input_tags` MUST be echoed if available.

#### Scenario: valid_tags content shape invalid
- **WHEN** `input.valid_tags` can be read but parsed result is not a top-level list of strings
- **THEN** the skill returns schema-compatible output with empty `remove_tags` and `add_tags` and a non-null `error` object

### Requirement: No implicit fallback on format mismatch
If `valid_tags_format` is explicitly set to `yaml` or `json`, and parsing fails, the skill MUST NOT attempt another format and MUST return error output per failure handling.

#### Scenario: Explicit json but invalid content
- **WHEN** `valid_tags_format=json` and the file cannot be parsed as JSON array of strings
- **THEN** the skill returns schema-compatible error output and does not try YAML parsing

### Requirement: auto format detection is opt-in
Only when `valid_tags_format=auto` is explicitly provided, the skill MAY try parsing in order `yaml -> json`, and the skill MUST NOT attempt this detection flow when `valid_tags_format` is omitted or explicitly set to `yaml` or `json`.

#### Scenario: auto detection
- **WHEN** `valid_tags_format=auto`
- **THEN** the skill tries `yaml`, then `json`; if both fail, returns schema-compatible error output

## ADDED Requirements

### Requirement: Structured valid_tags content
The parsed content of `input.valid_tags` MUST be a top-level array/list whose every element is a string.

#### Scenario: YAML list of strings
- **WHEN** `valid_tags_format=yaml` and the file is a YAML top-level list of strings
- **THEN** parsing and validation succeed

#### Scenario: JSON array of strings
- **WHEN** `valid_tags_format=json` and the file is a JSON top-level array of strings
- **THEN** parsing and validation succeed
