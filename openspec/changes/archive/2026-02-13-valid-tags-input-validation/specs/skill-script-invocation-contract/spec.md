## MODIFIED Requirements

### Requirement: SKILL.md 必须声明脚本调用时机
若发布目录保留运行时脚本，`tag-regulator/SKILL.md` MUST 明确该脚本的调用时机、输入输出约定与执行顺序。当前流程至少包括：
- 执行开始阶段：`valid_tags` 输入校验脚本
- 候选输出生成后：输出规范化脚本

#### Scenario: 调用点明确
- **WHEN** 维护者阅读 `tag-regulator/SKILL.md`
- **THEN** 能明确知道“开始阶段先校验 valid_tags，输出前再做规范化”

### Requirement: SKILL.md 必须提供无脚本回退
`tag-regulator/SKILL.md` MUST 提供脚本不可用时的等价回退步骤，且回退后输出仍满足既有契约（单 JSON、required keys、约束不变）。

#### Scenario: 运行环境无脚本能力
- **WHEN** skill 执行环境无法调用本地脚本
- **THEN** 按回退步骤完成 `valid_tags` 合法性校验与输出稳定化，并输出契约兼容结果

## ADDED Requirements

### Requirement: 启动阶段 valid_tags 校验脚本
`$tag-regulator` 在进入语义规范化前 MUST 先调用发布目录中的 valid_tags 校验脚本，以确认文件可按允许格式解析，且解析结果为字符串数组。

#### Scenario: 前置校验成功
- **WHEN** 校验脚本返回成功
- **THEN** skill 继续执行后续规范化与推断流程

#### Scenario: 前置校验失败
- **WHEN** 校验脚本返回失败
- **THEN** skill 立即走失败兜底并输出契约兼容错误 JSON，不进入后续语义流程
