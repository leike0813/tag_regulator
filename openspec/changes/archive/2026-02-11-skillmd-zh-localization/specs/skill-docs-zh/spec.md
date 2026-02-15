## ADDED Requirements

### Requirement: 发布包文档中文化
发布目录 `tag-regulator/` 内的文本文档 MUST 提供中文版本，并以中文为主要维护语言：
- `tag-regulator/SKILL.md` MUST 使用中文描述核心规则、流程与示例说明（代码标识符与 JSON/命令块保持原样）。
- `tag-regulator/README.md` MUST 使用中文描述发布包边界、使用方式与校验命令（命令行示例保持原样）。

#### Scenario: 文档可读性与一致性
- **WHEN** 维护者打开 `tag-regulator/SKILL.md` 与 `tag-regulator/README.md`
- **THEN** 主要说明文本为中文，且不改变字段名/路径/命令等技术要素

### Requirement: 后续文档改动以中文为准
后续对发布包内文本文档（至少包含 `tag-regulator/SKILL.md`、`tag-regulator/README.md`）的改动 MUST 以中文进行；若出现中英混杂，中文表述 MUST 作为权威版本。

#### Scenario: 语言规范落地
- **WHEN** 未来对 `tag-regulator/SKILL.md` 或 `tag-regulator/README.md` 进行修改
- **THEN** 新增/修改的说明文本采用中文，并保持与既有契约一致

### Requirement: 翻译不引入行为变化
本次中文化 MUST 为语义等价翻译，不得引入任何运行时行为变化：
- 不新增/删除输出字段
- 不改变默认行为与约束
- 不更改脚本/Schema/测试的功能逻辑（除非另有明确需求）

#### Scenario: 契约保持不变
- **WHEN** 对比中文化前后的 `tag-regulator/SKILL.md` 与 `tag-regulator/README.md`
- **THEN** 技术契约与示例结构保持一致，差异仅限语言表述层面
