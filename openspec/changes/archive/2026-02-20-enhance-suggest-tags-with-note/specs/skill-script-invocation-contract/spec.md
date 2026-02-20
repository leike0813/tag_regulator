## MODIFIED Requirements

### Requirement: SKILL.md 必须声明脚本调用时机
若发布目录保留运行时脚本，`tag-regulator/SKILL.md` MUST 明确该脚本的调用时机、输入输出约定与执行顺序。当前流程至少包括：
- 执行开始阶段：`valid_tags` 输入校验脚本
- 候选输出生成后：输出规范化脚本（需覆盖对象化 `suggest_tags` 的去重与稳定排序规则）

#### Scenario: 调用点明确
- **WHEN** 维护者阅读 `tag-regulator/SKILL.md`
- **THEN** 能明确知道“开始阶段先校验 valid_tags，输出前再做规范化（包含 `suggest_tags[].tag` 维度的稳定化）”

### Requirement: SKILL.md 必须提供无脚本回退
`tag-regulator/SKILL.md` MUST 提供脚本不可用时的等价回退步骤，且回退后输出仍满足既有契约（单 JSON、required keys、约束不变）。

#### Scenario: 运行环境无脚本能力
- **WHEN** skill 执行环境无法调用本地脚本
- **THEN** 按回退步骤完成 `valid_tags` 合法性校验与输出稳定化（包括对象化 `suggest_tags`），并输出契约兼容结果

## ADDED Requirements

### Requirement: SKILL.md 必须声明 tag_note_language 的作用域
`tag-regulator/SKILL.md` MUST 明确 `tag_note_language` 仅用于指定 `suggest_tags[].note` 的语言，不得影响其他输出字段或决策逻辑。

#### Scenario: 参数作用域说明清晰
- **WHEN** 维护者阅读参数说明
- **THEN** 能明确 `tag_note_language` 不影响 `remove_tags`、`add_tags`、`suggest_tags[].tag`、`warnings` 与 `error`
