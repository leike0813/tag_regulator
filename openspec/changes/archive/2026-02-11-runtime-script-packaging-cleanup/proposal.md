## Why

当前 `tag-regulator/` 发布目录中同时存在运行时与开发期脚本，但 `SKILL.md` 未明确脚本调用时机，导致“哪些文件属于发布必需”边界不清。需要通过一次变更明确发布准入规则：仅保留 skill 执行过程中实际会调用的脚本，其余迁出发布目录。

## What Changes

- 建立发布目录脚本准入规则：
  - 仅当脚本在 `$tag-regulator` 执行流程中有明确调用时机，才允许保留在 `tag-regulator/`。
  - 仅用于测试/CI/离线调试的脚本必须迁出 `tag-regulator/` 到开发工具目录。
- 对现有脚本做分类并落地迁移：
  - 保留候选：`tag-regulator/scripts/normalize_output.py`（用于最终输出的去重与稳定排序）。
  - 迁出候选：`tag-regulator/scripts/validate_output.py`、`tag-regulator/scripts/cli.py`、`tag-regulator/assets/output_schema.json`（若仅用于测试/CI校验）。
- 在 `tag-regulator/SKILL.md` 明确保留脚本的调用时机、调用前置条件与失败回退路径，避免“文档不提及导致 agent 不调用”的问题。
- 更新测试与开发文档，使迁移后的脚本路径与用途一致。
- **BREAKING**: 若脚本/Schema 路径调整，现有本地校验命令与测试导入路径将发生变化。

## Capabilities

### New Capabilities

- `runtime-script-governance`: 定义 Skill 发布目录脚本的准入规则与迁移策略（运行时必需才可保留，开发期脚本必须迁出）。
- `skill-script-invocation-contract`: 在 `SKILL.md` 中定义保留脚本的调用时机与执行契约（包括回退行为）。

### Modified Capabilities

<!-- None (new governance capability for this change). -->

## Impact

- 影响发布目录结构：`tag-regulator/` 中脚本与资产文件可能减少，仅保留运行时必需内容。
- 影响文档：`tag-regulator/SKILL.md` 与 `tag-regulator/README.md` 将补充“脚本用途与调用时机”说明。
- 影响开发工具链：测试/CI 所用校验脚本与 schema 路径将更新到开发目录。
