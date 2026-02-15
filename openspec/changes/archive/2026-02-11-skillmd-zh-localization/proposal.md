## Why

当前 `tag-regulator` 的发布包文档以英文为主，不利于团队后续持续迭代与一致理解（尤其是执行约束、默认行为与示例）。需要尽快将核心文档中文化，并明确后续文档改动以中文为准，降低沟通成本与误用风险。

## What Changes

- 将发布目录内的文本文档中文化：
  - `tag-regulator/SKILL.md`：完整中文化（保留所有代码标识符与 JSON 片段的结构与字段名不变）。
  - `tag-regulator/README.md`：中文化（命令行示例保持原样）。
- 明确文档语言规范：
  - 后续对发布包内文本文档（尤其是 `SKILL.md` / `README.md`）的改动以中文为准。
  - 非文档类内容（脚本、schema、测试、配置等）不进行中文化改写，除非另有明确需求。
- 不改变 skill 的行为约束与输出契约：仅做语言与表述层面的等价翻译，不引入新的功能/行为差异。

## Capabilities

### New Capabilities

- `skill-docs-zh`: 提供中文版本的 skill 发布包文档，并建立“后续文档改动以中文为准”的规范。

### Modified Capabilities

<!-- None (documentation-only change; no runtime behavior/spec requirement changes). -->

## Impact

- 影响范围仅限发布包内文本文档（`tag-regulator/`），不涉及脚本逻辑与运行时行为变更。
- 降低后续维护成本：中文文档更易被一致遵循，减少因误读而导致的契约违规（如 stdout 非 JSON、字段缺失、默认行为偏差等）。
