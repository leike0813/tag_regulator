## ADDED Requirements

### Requirement: 发布目录脚本准入
`tag-regulator/` 发布目录 MUST 仅包含 `$tag-regulator` 执行主路径中会实际调用的脚本。若脚本仅用于测试、CI、离线调试或文档示例，它 MUST NOT 留在发布目录中。

#### Scenario: 仅测试用途脚本
- **WHEN** 某脚本仅在 `pytest` 或离线校验中使用
- **THEN** 该脚本被迁出 `tag-regulator/` 并放入开发工具目录

### Requirement: 运行时必需脚本可保留
若脚本直接参与 skill 最终输出收敛（例如去重、稳定排序），且在 `SKILL.md` 中定义了调用时机与回退行为，则该脚本 MAY 保留在 `tag-regulator/`。

#### Scenario: 输出规范化脚本
- **WHEN** 脚本用于“最终输出前”的稳定排序与去重
- **THEN** 脚本可保留在发布目录并被文档明确引用

### Requirement: 开发工具迁移后可用
迁出发布目录的开发脚本与 schema MUST 在新目录中保持可执行，且 README/测试中的路径引用 MUST 同步更新。

#### Scenario: 路径同步
- **WHEN** 脚本从 `tag-regulator/` 迁移到开发目录
- **THEN** 本地命令与测试引用路径更新后仍能成功运行
