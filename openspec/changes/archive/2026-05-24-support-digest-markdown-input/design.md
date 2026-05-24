## Context

`tag-regulator` 当前仅消费 `metadata`、`input_tags` 与 `valid_tags`。上游 workflow 将可选提供 `digest_markdown` 文件输入，用于补足论文语义上下文。该输入属于增强信息，不应改变失败边界：主流程仍只对 `input_tags` 与 `valid_tags` 读取失败执行兜底错误返回。

## Goals / Non-Goals

**Goals:**
- 为 skill 增加可选 `digest_markdown` 输入声明（schema + runner + SKILL 文档）。
- 在推断流程中明确 digest 的作用域与优先级：仅补充 metadata，不突破受控词表约束。
- 明确 digest 读取失败策略：记录 warning 并忽略，主流程继续。

**Non-Goals:**
- 不新增输出字段（如 `digest_markdown_meta`）。
- 不修改输出 JSON schema。
- 不改变 `remove_tags` / `add_tags` / `suggest_tags` 现有结构与排序去重约束。

## Decisions

1) 可选输入建模
- 决策：`digest_markdown` 作为 `input` 下可选字符串路径，`x-input-source=file`，扩展名限制为 `.md`/`.markdown`。
- 备选：作为 inline 文本注入。
- 取舍：路径输入与现有 `valid_tags` 文件注入模式一致，更适配大文本内容。

2) digest 失败处理策略
- 决策：缺失/空值忽略；不可读或编码异常记录 warning 并忽略。
- 备选：统一静默忽略；或一律错误返回。
- 取舍：warning 方案兼顾可观测性与向后兼容，不中断批处理。

3) 推断优先级
- 决策：`valid_tags` 约束最高；`input_tags` + `metadata` 为主证据；`digest_markdown` 为补充证据。
- 备选：digest 与 metadata 同权。
- 取舍：保持现有语义稳定，避免 digest 对既有行为造成过强扰动。

## Risks / Trade-offs

- [Risk] digest 文本噪声导致误推断 → Mitigation: 明确“补充证据”定位，并继续使用保守推断与 warnings。
- [Risk] 调用方误以为 digest 为必需输入 → Mitigation: input schema 与 SKILL 文档显式声明可选。
- [Risk] digest 内容诱导越过词表写入 `add_tags` → Mitigation: specs 与 SKILL 均重申 routing 约束不变。

## Migration Plan

1. 创建并完善本 change 的 proposal/specs/design/tasks。
2. 更新 input schema、runner prompt 与 SKILL 文档。
3. 新增/更新测试（schema、runner、文档关键约束）。
4. 运行 `pytest` 与 `mypy` 完成回归。
5. 通过 `openspec validate --type change support-digest-markdown-input --strict --json` 验证变更工件。

## Open Questions

- None.
