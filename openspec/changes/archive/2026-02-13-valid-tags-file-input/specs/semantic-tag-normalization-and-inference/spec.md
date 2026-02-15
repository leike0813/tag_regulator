## MODIFIED Requirements

### Requirement: Controlled vocabulary constraint
The skill MUST treat the parsed contents of `input.valid_tags` as the controlled vocabulary (`valid_tags`), and MUST ensure that every tag in `add_tags` is a member of that parsed `valid_tags` set.

#### Scenario: Add tag in vocabulary
- **WHEN** the skill decides a new tag should be added
- **THEN** it only adds the tag to `add_tags` if it exists in the parsed `valid_tags`
