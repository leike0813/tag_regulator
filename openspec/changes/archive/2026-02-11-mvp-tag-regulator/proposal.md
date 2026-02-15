## Why

We need a reliable, repeatable way to regulate Zotero tags with a **controlled vocabulary** (`valid_tags`) and a consistent naming standard, reducing noise and manual cleanup. This is needed now because downstream automation requires stable tags and strict, machine-consumable outputs.

This project is an **Agent Skill** (not a traditional deterministic code-only system): the core value comes from leveraging LLM semantic understanding to infer and normalize tags; small scripts are only auxiliary for validation and strict output conformance.

## What Changes

- Introduce an Agent Skill package that, given prompt-embedded payload (`metadata`, `input_tags`, `valid_tags`, `infer_tag`), produces a single JSON object on stdout describing tag changes.
- Implement **valid-tags-constrained normalization**:
  - Any tag to be added (`add_tags`) MUST be a member of `valid_tags`.
  - Tags that are semantically relevant and follow the naming standard but are not present in `valid_tags` are emitted as `suggest_tags` for later vocabulary governance.
- Implement **semantic inference** (MVP includes inferred tags):
  - When `infer_tag` is enabled and `metadata` is present and non-empty, infer candidate tags using semantic understanding over high-priority fields (e.g., `title`, `abstract`, `keywords`, `conference_name`, `publication_title`).
  - Inferred tags MUST be constrained by `valid_tags` (else go to `suggest_tags`).
- Enforce the hard runtime contract (from `AGENTS.md`):
  - Non-interactive, batch-safe defaults (no questions during execution).
  - stdout outputs **only one JSON object** (no logs, no extra text).
  - Output JSON MUST contain: `remove_tags`, `add_tags`, `suggest_tags`, `provenance.generated_at` (UTC ISO-8601), `warnings` (array), `error` (object|null).
  - Response MUST echo back `metadata` and `input_tags` for anti-mixup alignment.
  - If reading `input_tags` or `valid_tags` fails, return schema-compatible JSON with `error` populated and empty `remove_tags`/`add_tags`.

## Capabilities

### New Capabilities

- `tag-regulator-skill-contract`: Define the skill I/O contract, default behaviors, failure modes, and strict stdout JSON-only schema (including required echo fields).
- `semantic-tag-normalization-and-inference`: Perform semantic-driven tag normalization and metadata-based inference under the hard constraint that any added normalized tag must be within `valid_tags`, otherwise emitted as `suggest_tags`.

### Modified Capabilities

<!-- None (no existing specs yet). -->

## Impact

- Primary deliverable is the **publishable skill package** under the repository root: `tag-regulator/`.
  - `tag-regulator/SKILL.md` will be the main implementation surface (rich prompting + complete guidance + invariants).
  - Optional `tag-regulator/scripts/` may be added only as an auxiliary layer for strict output validation/normalization (e.g., JSON schema checks, stable ordering/dedup, timestamp formatting).
- Downstream implementation and verification will be organized via OpenSpec artifacts (specs/design/tasks) anchored to the two capabilities above.
