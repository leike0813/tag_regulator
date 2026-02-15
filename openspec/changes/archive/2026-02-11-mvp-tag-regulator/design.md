## Context

This repository implements **$tag-regulator** as an **Agent Skill**. The primary deliverable is a publishable skill package under `tag-regulator/`, where `tag-regulator/SKILL.md` provides rich, executable guidance for an LLM agent to:

- semantically normalize user-provided tags (`input_tags`) under a hard controlled vocabulary constraint (`valid_tags`)
- infer additional tags from paper metadata (`metadata`) when `infer_tag` is enabled

The runtime contract is strict (per `AGENTS.md`):

- Non-interactive execution (no asking questions; default behaviors must resolve ambiguity).
- stdout must be **exactly one JSON object** (no logs, no extra text).
- Output schema is fixed: `remove_tags`, `add_tags`, `suggest_tags`, `provenance.generated_at` (UTC ISO-8601), `warnings`, `error`, plus echo fields `metadata` and `input_tags`.
- Any failure to read `input_tags` or `valid_tags` must return schema-compatible JSON with `error` populated and empty `remove_tags`/`add_tags`.

The tag naming rules and controlled vocabulary guidance live in:
- `references/tag_standard.md`
- `references/valid_tag_list.md`

MVP scope (proposal): valid-tags-constrained normalization + inferred tags.

## Goals / Non-Goals

**Goals:**
- Ship a minimal, publishable Agent Skill in `tag-regulator/` whose `SKILL.md` is sufficient to consistently produce schema-valid JSON outputs.
- Make semantic-driven decisions (normalization + inference) while ensuring **all normalized additions** are members of `valid_tags`.
- Provide clear default behavior for ambiguity and missing inputs without interactive prompts.
- Keep results stable and machine-consumable (single JSON; required keys always present; deterministic ordering rules described).

**Non-Goals:**
- Building a fully deterministic tag regulator driven purely by regex/string rules (scripts may assist validation only).
- Expanding/maintaining the controlled vocabulary itself (out of scope; surfaced via `suggest_tags`).
- Writing back to Zotero or any external system.
- Achieving perfect semantic tagging; MVP prioritizes correctness under constraints and safe defaults.

## Decisions

1) **Primary implementation surface is `tag-regulator/SKILL.md`**

Rationale: The core tasks (metadata-based inference and semantic normalization) require language understanding. The skill must therefore encode:
- the contract (I/O + defaults + failure modes)
- the decision procedure (step-by-step normalization/inference)
- guardrails (no extra stdout text; no hallucinated tags outside `valid_tags` for `add_tags`)
- examples (input payload → output JSON) to anchor behavior

Alternative considered: implement most logic as Python and keep SKILL minimal. Rejected for MVP because semantic mapping quality would degrade and the project goal is an Agent Skill.

2) **Hard constraint: `add_tags ⊆ valid_tags`**

Rationale: This is a core project constraint and enables downstream systems to trust the regulated output. Any semantically relevant but out-of-vocabulary tag must be routed to `suggest_tags` (after enforcing naming conventions).

Alternative considered: allow adding out-of-vocabulary tags if they conform to naming rules. Rejected; it defeats “controlled” vocabulary and causes tag explosion.

3) **Semantic normalization is guided by `valid_tags` as the canonical target set**

Decision procedure (to be specified in SKILL.md and later in specs):
- Treat `valid_tags` entries as the only “allowed normalized tags”.
- For each `input_tag`, use semantic understanding plus naming rules to map it to:
  - an existing valid tag (preferred), or
  - a suggested tag (normalized to naming standard) when not present in `valid_tags`, or
  - nothing (when the input is noise / irrelevant)
- Output a diff:
  - `remove_tags`: tags to remove from the original `input_tags`
  - `add_tags`: valid tags to add
  - `suggest_tags`: normalized-but-not-valid tags (for later governance), plus inferred-but-not-valid candidates

Alternative considered: only normalize by exact/case-insensitive matching. Rejected because it cannot resolve synonyms, paraphrases, or implicit semantics.

4) **Inference (`infer_tag`) uses metadata with strict defaults**

Defaults (must match `AGENTS.md`):
- If `metadata` missing or empty: force `infer_tag=false` (ignore user input).
- If `infer_tag` is not parseable as true/false from prompt semantics: default to `true`.

Inference sources (priority): `title`, `abstract`, `keywords`, `conference_name`, `publication_title` (others optional).

Output constraints:
- If inferred tag is in `valid_tags`: include in `add_tags` (deduped).
- Otherwise: include in `suggest_tags` (normalized to naming standard) with a warning when confidence is low.

Alternative considered: always infer regardless of metadata presence. Rejected by explicit default rules.

5) **Strict output shaping + determinism rules**

To reduce brittleness in batch pipelines:
- Always emit all required keys (even if empty).
- Include `provenance.generated_at` in UTC ISO-8601.
- Echo `metadata` and `input_tags` exactly as received.
- Avoid any non-JSON stdout (no Markdown, no code fences, no explanations).

Array ordering (to be defined and implemented consistently):
- `remove_tags`: preserve the order of appearance in `input_tags`.
- `add_tags` / `suggest_tags`: stable ordering (e.g., first by first-appearance during reasoning, then lexicographic as a tie-breaker) and no duplicates.

Alternative considered: fully sort all arrays lexicographically. Rejected for `remove_tags` because it can reduce traceability to the original inputs.

6) **Scripts are auxiliary and live under `tag-regulator/scripts/` (optional for MVP, but recommended)**

Purpose: enforce strict conformance and support automated testing without replacing the semantic core.

Candidate scripts:
- JSON schema validator for stdout payload shape
- normalizer/formatter that enforces deduping and ordering rules

These scripts are used in local tests/CI, not as the primary runtime decision engine.

7) **Publishable skill package boundaries**

Only ship what is needed to run the skill:
- `tag-regulator/SKILL.md`
- optionally `tag-regulator/scripts/*` for validation/formatting

Development references remain outside the package (e.g., `references/`, `openspec/`) to keep the publish directory clean as required.

## Risks / Trade-offs

- [Non-deterministic LLM behavior] → Mitigation: encode a strict step-by-step procedure, include multiple anchored examples, and keep `add_tags` constrained to `valid_tags`.
- [Over-inference / hallucinated tags] → Mitigation: require “in-vocab only” for `add_tags`, route out-of-vocab to `suggest_tags`, and emit `warnings` on low confidence.
- [Ambiguity in mapping synonyms to valid tags] → Mitigation: prefer conservative behavior (don’t add unless confident), add warnings, and rely on `suggest_tags` to surface gaps in the vocabulary.
- [Schema violations / extra stdout text breaks pipelines] → Mitigation: emphasize JSON-only output in SKILL.md, provide a validator script, and add fixtures tests in later tasks.
