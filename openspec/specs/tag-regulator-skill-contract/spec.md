# tag-regulator-skill-contract Specification

## Purpose
TBD - created by archiving change mvp-tag-regulator. Update Purpose after archive.
## Requirements
### Requirement: Input payload fields
The skill SHALL read a prompt-embedded payload containing optional `metadata`, optional `input_tags`, and optional `infer_tag`. The Runner input files `input.valid_tags` and `input.digest_markdown` SHALL be optional.

If `input_tags` is missing, the skill MUST treat it as an empty string array for processing and output echoing.

#### Scenario: Missing input_tags
- **WHEN** the prompt does not contain `input_tags`
- **THEN** the skill treats `input_tags` as `[]` and still includes `"input_tags": []` in output

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

### Requirement: Anti-mixup echoing
The output `metadata` and `input_tags` values MUST match the received payload exactly (no rewriting, normalization, truncation, or structural changes).

#### Scenario: Echo alignment
- **WHEN** the input payload contains `metadata` and `input_tags`
- **THEN** the output JSON includes the same values for `metadata` and `input_tags`

### Requirement: Default infer_tag behavior
The skill MUST determine effective tag inference according to available evidence and mode:

1) In controlled vocabulary mode, `input_tags` normalization MUST still run when `input_tags` exist, regardless of `infer_tag`.
2) In controlled vocabulary mode, explicit `infer_tag=false` MUST disable metadata/digest-driven additional inference.
3) In controlled vocabulary mode, if `infer_tag` is missing or cannot be interpreted and metadata or readable digest evidence exists, inference defaults to enabled.
4) In pure inference mode, `infer_tag=false` MUST NOT disable inference from available `input_tags`, metadata, or readable digest evidence.
5) If no usable evidence exists, the skill MUST return an `insufficient_input` error.

#### Scenario: Digest-only inference evidence
- **WHEN** `metadata` is missing or empty, readable non-empty `digest_markdown` is provided, and inference is otherwise enabled
- **THEN** the skill may infer tags from digest evidence

#### Scenario: Controlled mode explicit false
- **WHEN** `valid_tags` is provided and `infer_tag=false`
- **THEN** the skill still normalizes existing `input_tags` but does not add metadata/digest-only inferred tags

#### Scenario: Pure inference explicit false
- **WHEN** `valid_tags` is absent, `infer_tag=false`, and any usable evidence exists
- **THEN** the skill still produces pure inference `suggest_tags` when relevant

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

### Requirement: tag_note_language scope isolation
`tag_note_language` MUST only affect the language expression of `suggest_tags[].note`, and MUST NOT affect the values or decision logic of `remove_tags`, `add_tags`, `suggest_tags[].tag`, `warnings`, or `error`.

#### Scenario: Note language only affects note
- **WHEN** `tag_note_language` is provided as `en-US`
- **THEN** `suggest_tags[].note` is expressed in English intent while other output fields keep their original decision behavior

### Requirement: Optional digest_markdown is non-fatal
`digest_markdown` input MUST be treated as optional enhancement context. If it is missing, empty, unreadable, or has encoding errors, the skill MUST continue execution without failing the run.

#### Scenario: Missing digest_markdown
- **WHEN** `digest_markdown` is not provided
- **THEN** the skill continues normal processing using existing evidence sources and does not return error

#### Scenario: Unreadable digest_markdown
- **WHEN** `digest_markdown` is provided but file reading fails due to permissions/path/encoding issues
- **THEN** the skill appends a warning and ignores digest context while continuing the run

### Requirement: Pure inference output shape
When `input.valid_tags` is absent, the output JSON MUST still include all required keys and MUST set:
- `remove_tags=[]`
- `add_tags=[]`

The skill MAY include normalized candidates in `suggest_tags`.

#### Scenario: Pure inference suggestions
- **WHEN** the skill runs without `input.valid_tags` and identifies relevant normalized tag candidates
- **THEN** it emits those candidates in `suggest_tags`, keeps `remove_tags=[]` and `add_tags=[]`, and sets `error=null`

### Requirement: Insufficient input failure
If `metadata`, readable non-empty `digest_markdown`, `input_tags`, and `valid_tags` are all absent or empty, the skill MUST return schema-compatible output with:
- `input_tags=[]`
- `remove_tags=[]`
- `add_tags=[]`
- `suggest_tags=[]`
- `error.type="insufficient_input"`

#### Scenario: No usable inputs
- **WHEN** the payload provides no metadata, no input tags, no valid_tags, and no readable non-empty digest markdown
- **THEN** the skill returns an `insufficient_input` error JSON and does not attempt semantic inference

