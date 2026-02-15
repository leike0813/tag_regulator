## MODIFIED Requirements

### Requirement: Input payload fields
The skill SHALL read a prompt-embedded payload containing `metadata`, `input_tags`, and `infer_tag`, and SHALL read the controlled vocabulary from the Runner input file `input.valid_tags` (a file path).

#### Scenario: Payload present and valid_tags file present
- **WHEN** the prompt contains a payload with `metadata`, `input_tags`, and optionally `infer_tag`, and Runner provides `input.valid_tags` as a readable file path
- **THEN** the skill treats these sources as the only source of truth for the run

### Requirement: Failure handling for missing input_tags or valid_tags
If reading `input_tags` fails OR reading/parsing `input.valid_tags` fails (missing/unreadable/invalid type/encoding/format error), the skill MUST return schema-compatible output with:
- `remove_tags=[]`
- `add_tags=[]`
- `error` set to a non-null object describing the failure

`warnings` MUST still be present (may be empty), `provenance.generated_at` MUST still be present, and `metadata`/`input_tags` MUST be echoed if available.

#### Scenario: valid_tags file missing
- **WHEN** `input.valid_tags` cannot be read as a file
- **THEN** the skill returns schema-compatible output with empty `remove_tags` and `add_tags` and a non-null `error` object

## ADDED Requirements

### Requirement: valid_tags_format parameter
The skill MUST support a `valid_tags_format` parameter to specify the format of the `input.valid_tags` file. Supported values MUST include: `yaml`, `json`, `txt`, `auto`. The default MUST be `yaml`.

#### Scenario: Default format
- **WHEN** `valid_tags_format` is not provided
- **THEN** the skill parses `input.valid_tags` as `yaml`

### Requirement: No implicit fallback on format mismatch
If `valid_tags_format` is explicitly set to `yaml`, `json`, or `txt`, and parsing fails, the skill MUST NOT attempt to parse as a different format and MUST return an error per failure handling.

#### Scenario: Explicit yaml but invalid content
- **WHEN** `valid_tags_format=yaml` and the file content is not valid YAML list of strings
- **THEN** the skill returns a schema-compatible error output and does not try json/txt parsing

### Requirement: auto format detection is opt-in
If and only if `valid_tags_format=auto` is explicitly provided, the skill MAY attempt to detect the file format by trying parsing in the following order: `yaml -> json -> txt`. The skill MUST record a warning indicating `auto` was used and which format was selected.

#### Scenario: auto detection
- **WHEN** `valid_tags_format=auto`
- **THEN** the skill tries `yaml`, then `json`, then `txt`, and records a warning about the selected format
