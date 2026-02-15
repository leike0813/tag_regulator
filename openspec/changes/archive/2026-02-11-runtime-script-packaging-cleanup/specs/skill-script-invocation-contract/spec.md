## ADDED Requirements

### Requirement: SKILL.md 必须声明脚本调用时机
若发布目录保留运行时脚本，`tag-regulator/SKILL.md` MUST 明确该脚本的调用时机、输入输出约定与执行顺序。

#### Scenario: 调用点明确
- **WHEN** 维护者阅读 `tag-regulator/SKILL.md`
- **THEN** 能明确知道脚本在“候选 JSON 生成后、最终输出前”被调用

### Requirement: SKILL.md 必须提供无脚本回退
`tag-regulator/SKILL.md` MUST 提供脚本不可用时的等价回退步骤，且回退后输出仍满足既有契约（单 JSON、required keys、约束不变）。

#### Scenario: 运行环境无脚本能力
- **WHEN** skill 执行环境无法调用本地脚本
- **THEN** 按回退步骤完成去重与稳定排序，并输出契约兼容结果

### Requirement: 调用脚本不得破坏输出契约
脚本调用过程 MUST NOT 导致最终 stdout 出现多段文本；最终响应仍必须是单个 JSON 对象。

#### Scenario: 含脚本执行的正常流程
- **WHEN** 运行时调用了规范化脚本
- **THEN** 最终 stdout 仍仅包含一个 JSON 对象且字段完整
