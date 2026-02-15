## Context

`tag-regulator/` 是 skill 发布目录，原则上应只包含运行时必需文件。当前目录中存在 `scripts/validate_output.py`、`scripts/cli.py` 与 `assets/output_schema.json`，但 `SKILL.md` 未定义这些文件在 `$tag-regulator` 执行流程中的调用时机，导致发布边界与调用契约不清晰。

本次变更要同时解决两个问题：
1) 发布目录准入规则：运行时用不到的脚本不得留在发布目录；
2) 若保留脚本：必须在 `SKILL.md` 明确调用时机、前置条件与失败回退行为。

## Goals / Non-Goals

**Goals:**
- 建立可执行的“发布目录脚本准入规则”并落地到当前文件结构。
- 明确保留脚本的最小集合与用途（面向 skill 运行时）。
- 将开发/测试专用脚本迁出 `tag-regulator/`，并更新测试与文档路径。
- 在 `SKILL.md` 中新增脚本调用契约，避免 agent 忽略脚本。

**Non-Goals:**
- 不改变 tag 语义推断与规范化的业务规则本身。
- 不新增复杂的运行时编排系统；仅做目录治理和调用约定。
- 不对非相关脚本做功能增强（除迁移导致的最小路径修正外）。

## Decisions

1) **脚本准入判定标准**
- 判定为“可保留在发布目录”的必要条件：
  - 在 `$tag-regulator` 执行主路径中有明确调用点；
  - 对最终输出质量有直接作用（例如去重、稳定排序、结构收敛）；
  - `SKILL.md` 中存在可执行调用约定。
- 否则归类为开发工具并迁出发布目录。

2) **当前脚本保留/迁移决策**
- 保留：`tag-regulator/scripts/normalize_output.py`
  - 用途：对已生成输出执行去重与稳定排序，保证批处理结果稳定。
  - 运行时位置：在“生成候选 JSON 后、最终输出前”调用。
- 迁出：`tag-regulator/scripts/validate_output.py`、`tag-regulator/scripts/cli.py`、`tag-regulator/assets/output_schema.json`
  - 用途：开发/测试/CI 校验，不属于技能执行主路径。
  - 目标位置：仓库级开发工具目录（如 `dev-tools/tag-regulator/`）。

3) **`SKILL.md` 调用契约**
- 新增“脚本调用时机”段落，明确：
  - 调用点：输出最终落地前；
  - 输入/输出：对临时 JSON 文件进行规范化后再作为最终输出；
  - 失败回退：脚本不可用时，使用文档内等价的手工规则（去重+稳定排序）并记录 `warnings`。

4) **迁移后兼容**
- 更新 `README.md` 的本地开发命令示例到新路径。
- 更新测试导入路径，确保 `pytest` 与 `mypy` 仍可运行。

## Risks / Trade-offs

- [运行环境无法执行脚本] → Mitigation: 在 `SKILL.md` 提供严格等价的无脚本回退流程，并保持输出契约不变。
- [迁移后开发命令失效] → Mitigation: 同步更新 README、测试与 CI 命令路径。
- [脚本边界再次漂移] → Mitigation: 在 spec 中固化“发布目录准入标准”，后续变更必须显式声明用途与调用点。

## Migration Plan

1) 在仓库新增开发工具目录并迁移测试/校验脚本与 schema。
2) 在发布目录仅保留运行时规范化脚本，并修正引用。
3) 更新 `SKILL.md` 与 `README.md`，补充调用时机和路径。
4) 跑通测试与类型检查，确认无行为回归。

## Open Questions

- 开发工具目录命名采用 `dev-tools/tag-regulator/` 还是 `tools/tag-regulator-dev/`。本次默认采用 `dev-tools/tag-regulator/`。
