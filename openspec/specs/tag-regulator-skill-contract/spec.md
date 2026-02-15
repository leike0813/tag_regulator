# tag-regulator-skill-contract Specification

## Purpose
TBD - created by archiving change mvp-tag-regulator. Update Purpose after archive.
## Requirements
### Requirement: Input payload fields
The skill SHALL read a prompt-embedded payload containing `metadata`, `input_tags`, and `infer_tag`, and SHALL read the controlled vocabulary from the Runner input file `input.valid_tags` (file path). The skill SHALL also read `valid_tags_format` with supported values `yaml`, `json`, `auto` (default `yaml`).

#### Scenario: Payload present and valid_tags file present
- **WHEN** the prompt contains `metadata`, `input_tags`, optional `infer_tag`, and optional `valid_tags_format`, and Runner provides a readable `input.valid_tags` file path
- **THEN** the skill treats these as the only source of truth for the run

### Requirement: Non-interactive execution
The skill MUST run in non-interactive mode and MUST NOT ask the user to make decisions during execution. Any ambiguity MUST be resolved by default behavior and the skill MUST continue to completion.

#### Scenario: Ambiguous mapping
- **WHEN** the skill encounters an ambiguous case (e.g., multiple plausible normalizations)
- **THEN** the skill chooses a conservative default behavior and proceeds without asking questions

### Requirement: JSON-only stdout
The skill MUST write exactly one JSON object to stdout and MUST NOT emit any additional text (including logs, explanations, Markdown, or multiple JSON blocks).

#### Scenario: Successful run
- **WHEN** the skill completes successfully
- **THEN** stdout contains exactly one JSON object and nothing else

### Requirement: Required output keys
The output JSON MUST always include the following keys (present even when empty):
- `remove_tags` (array)
- `add_tags` (array)
- `suggest_tags` (array)
- `provenance.generated_at` (string, UTC ISO-8601)
- `warnings` (array)
- `error` (object|null)

The output JSON MUST also echo back:
- `metadata` (exactly as received)
- `input_tags` (exactly as received)

#### Scenario: Minimal empty output
- **WHEN** no changes are needed and no tags are inferred
- **THEN** the output still contains all required keys, with empty arrays and `error=null`, and includes echoed `metadata` and `input_tags`

### Requirement: Anti-mixup echoing
The output `metadata` and `input_tags` values MUST match the received payload exactly (no rewriting, normalization, truncation, or structural changes).

#### Scenario: Echo alignment
- **WHEN** the input payload contains `metadata` and `input_tags`
- **THEN** the output JSON includes the same values for `metadata` and `input_tags`

### Requirement: Default infer_tag behavior
The skill MUST determine whether tag inference is enabled according to the following rules:
1) If `metadata` is missing or empty, inference MUST be disabled (`infer_tag=false`) regardless of user intent.
2) If the user explicitly provides `infer_tag` and it can be interpreted as true/false, the skill MUST use that meaning.
3) If `infer_tag` is explicitly provided but cannot be interpreted as true/false, inference MUST default to enabled (`infer_tag=true`).
4) If `infer_tag` is not provided and `metadata` is present and non-empty, inference MUST default to enabled (`infer_tag=true`).

#### Scenario: Missing metadata disables inference
- **WHEN** `metadata` is missing or empty
- **THEN** the skill treats inference as disabled and does not attempt to infer tags

### Requirement: Failure handling for missing input_tags or valid_tags
If reading `input_tags` fails OR reading/parsing/validating `input.valid_tags` fails (missing/unreadable/invalid type/encoding/format/content shape error), the skill MUST return schema-compatible output with:
- `remove_tags=[]`
- `add_tags=[]`
- `error` set to a non-null object describing the failure

`warnings` MUST still be present (may be empty), `provenance.generated_at` MUST still be present, and `metadata`/`input_tags` MUST be echoed if available.

#### Scenario: valid_tags content shape invalid
- **WHEN** `input.valid_tags` can be read but parsed result is not a top-level list of strings
- **THEN** the skill returns schema-compatible output with empty `remove_tags` and `add_tags` and a non-null `error` object

### Requirement: Error object shape (minimal)
When `error` is non-null, it MUST be a JSON object that includes:
- `type` (string)
- `message` (string)

#### Scenario: Error emitted
- **WHEN** an input read/parse failure occurs
- **THEN** `error` is an object containing `type` and `message`

### Requirement: Provenance timestamp
The skill MUST set `provenance.generated_at` to a UTC ISO-8601 timestamp with `Z` suffix.

#### Scenario: Timestamp format
- **WHEN** the skill produces output
- **THEN** `provenance.generated_at` is a string in UTC ISO-8601 format ending with `Z`

### Requirement: valid_tags_format parameter
The skill MUST support a `valid_tags_format` parameter to specify the format of the `input.valid_tags` file. Supported values MUST include: `yaml`, `json`, `txt`, `auto`. The default MUST be `yaml`.

#### Scenario: Default format
- **WHEN** `valid_tags_format` is not provided
- **THEN** the skill parses `input.valid_tags` as `yaml`

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

### Requirement: Structured valid_tags content
The parsed content of `input.valid_tags` MUST be a top-level array/list whose every element is a string.

#### Scenario: YAML list of strings
- **WHEN** `valid_tags_format=yaml` and the file is a YAML top-level list of strings
- **THEN** parsing and validation succeed

#### Scenario: JSON array of strings
- **WHEN** `valid_tags_format=json` and the file is a JSON top-level array of strings
- **THEN** parsing and validation succeed

