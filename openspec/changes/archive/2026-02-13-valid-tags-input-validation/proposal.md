## Why

当前流程里，`valid_tags` 一旦被错误地按“无结构纯文本”读取，可能把损坏内容误当成合法词表，直接污染 `add_tags` 结果。现在我们已经收紧输入策略，只允许结构化格式（YAML/JSON），需要补上一个确定性的运行时校验脚本，把风险挡在流程入口。

## What Changes

- 新增运行时脚本 `tag-regulator/scripts/validate_valid_tags.py`，用于校验 `valid_tags` 文件合法性。
  - 支持格式：`yaml`、`json`、`auto`（`auto` 仅按 `yaml -> json` 尝试）。
  - 严格要求：解析结果必须是“顶层字符串数组”。
- 更新 `tag-regulator/SKILL.md`：在执行开始阶段明确“先调用校验脚本，再进入语义规范化流程”。
- 更新 Skill 输入契约与发布资产：
  - 移除 `txt` 格式入口（参数枚举、输入 schema 扩展名、文档约定）。
  - 保持失败兜底语义不变（校验失败直接返回契约兼容错误 JSON）。
- 增加测试覆盖：覆盖 YAML/JSON 合法输入、结构错误、格式不匹配与 `auto` 分支行为。

## Capabilities

### New Capabilities

<!-- None -->

### Modified Capabilities

- `tag-regulator-skill-contract`: 收紧 `valid_tags_format` 与 `valid_tags` 文件解析约束（仅 YAML/JSON，且必须为字符串数组）。
- `skill-script-invocation-contract`: 增加“执行开始时调用 valid_tags 校验脚本”的运行时调用契约。

## Impact

- 影响文件：
  - `tag-regulator/scripts/`（新增校验脚本）
  - `tag-regulator/SKILL.md`（新增前置校验调用时机）
  - `tag-regulator/assets/input.schema.json`
  - `tag-regulator/assets/parameter.schema.json`
  - `AGENTS.md`
  - `tests/` 与 `dev-tools/tag-regulator/scripts/validate_output.py`（同步格式约束）
- 行为影响：`txt` 词表输入不再被接受；校验失败更早、失败原因更确定。
