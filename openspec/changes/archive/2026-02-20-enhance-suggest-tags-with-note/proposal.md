## Why

当前 `suggest_tags` 仅返回字符串，调用方无法获知每个建议 tag 的语义解释，影响人工审阅与后续词表治理效率。需要把建议项升级为结构化对象，并允许显式指定解释语言，以支持多语言工作流。

## What Changes

- 将输出字段 `suggest_tags` 从 `string[]` 升级为对象数组，单项结构至少包含：
  - `tag`：建议新增的 tag 本体
  - `note`：Agent 对该 tag 含义的解释说明
- 新增参数 `tag_note_language`（字符串）用于指定 `suggest_tags[].note` 的语言语义；推荐 BCP 47 形式（如 `zh-CN`、`en-US`），但不强制格式校验。
- 在 `SKILL.md` 中明确：`tag_note_language` **仅影响** `suggest_tags[].note` 的语言，不影响其他输出字段或规范化决策。
- 更新输出契约、示例与排序/去重约束描述，使对象数组输出在批处理场景下保持稳定。
- **BREAKING**: `suggest_tags` 输出类型由字符串数组变为对象数组，现有消费者需要适配新结构。

## Capabilities

### New Capabilities

<!-- None -->

### Modified Capabilities

- `tag-regulator-skill-contract`: 调整 `suggest_tags` 输出结构定义，并新增 `tag_note_language` 参数契约及作用域约束。
- `semantic-tag-normalization-and-inference`: 调整 OOV 建议输出语义，要求建议项包含 `tag` 与解释性 `note`，并约束 `note` 语言来源于 `tag_note_language`。
- `skill-script-invocation-contract`: 更新输出规范化脚本契约，确保对象化 `suggest_tags` 的稳定排序/去重规则被明确。

## Impact

- 影响规格与文档：`openspec/specs/*` 对应能力条目、`tag-regulator/SKILL.md`、示例 payload/输出。
- 影响运行时资产：`tag-regulator/assets/output.schema.json`、`tag-regulator/assets/parameter.schema.json`、`tag-regulator/assets/runner.json` 需同步更新。
- 影响脚本与测试：`tag-regulator/scripts/normalize_output.py`、`dev-tools/tag-regulator/scripts/validate_output.py`、相关 fixtures/tests 需适配新结构。
