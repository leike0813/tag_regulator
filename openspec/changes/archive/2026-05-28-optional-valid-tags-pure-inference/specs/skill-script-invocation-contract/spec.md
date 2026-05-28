## MODIFIED Requirements

### Requirement: SKILL.md 必须声明脚本调用时机
若发布目录保留运行时脚本，`tag-regulator/SKILL.md` MUST 明确该脚本的调用时机、输入输出约定与执行顺序。当前流程至少包括：
- 执行开始阶段：当且仅当提供 `valid_tags` 时调用输入校验脚本
- 候选输出生成后：输出规范化脚本（需覆盖对象化 `suggest_tags` 的去重与稳定排序规则）

#### Scenario: 调用点明确
- **WHEN** 维护者阅读 `tag-regulator/SKILL.md`
- **THEN** 能明确“有 valid_tags 才先校验 valid_tags，输出前总是做规范化（包含 `suggest_tags[].tag` 维度的稳定化）”

### Requirement: SKILL.md 必须提供无脚本回退
`tag-regulator/SKILL.md` MUST 提供脚本不可用时的等价回退步骤。若 `valid_tags` 缺失，回退步骤 MUST 不要求执行 valid_tags 文件校验。

#### Scenario: 运行环境无脚本能力且无 valid_tags
- **WHEN** skill 执行环境无法调用本地脚本且没有提供 `valid_tags`
- **THEN** skill 跳过 valid_tags 文件校验，仍完成纯推断输出稳定化并输出契约兼容结果

### Requirement: 启动阶段 valid_tags 校验脚本
`$tag-regulator` 在进入受控词表语义规范化前 MUST 先调用发布目录中的 valid_tags 校验脚本，以确认文件可按允许格式解析，且解析结果为字符串数组。未提供 `valid_tags` 时 MUST NOT 调用该脚本。

#### Scenario: 前置校验成功
- **WHEN** 提供了 `valid_tags` 且校验脚本返回成功
- **THEN** skill 继续执行受控词表规范化与推断流程

#### Scenario: 无 valid_tags
- **WHEN** 未提供 `valid_tags`
- **THEN** skill 跳过 valid_tags 校验脚本并进入纯推断模式

#### Scenario: 前置校验失败
- **WHEN** 提供了 `valid_tags` 且校验脚本返回失败
- **THEN** skill 立即走失败兜底并输出契约兼容错误 JSON，不进入后续语义流程
