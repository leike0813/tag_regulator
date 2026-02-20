## Context

当前 `suggest_tags` 是 `string[]`，只能表达“建议新增什么 tag”，无法表达“为什么建议这个 tag”。在词表治理与人工复核环节，这会导致上下文缺失。  
本次变更需要把 `suggest_tags` 升级为对象数组，并新增 `tag_note_language` 参数来控制说明语言，同时保证该参数不影响其他业务输出。

## Goals / Non-Goals

**Goals:**
- 将 `suggest_tags` 升级为结构化对象数组，至少包含 `tag` 与 `note`。
- 引入 `tag_note_language` 参数（自由字符串语义，推荐 BCP 47）并限定其仅作用于 `suggest_tags[].note`。
- 保持现有核心约束不变：`add_tags ⊆ valid_tags`、单 JSON 输出、失败兜底行为。
- 明确对象化 `suggest_tags` 的去重与稳定排序规则，确保批处理结果可复现。

**Non-Goals:**
- 不改变 tag 规范化/推断的语义策略本身。
- 不新增对 `tag_note_language` 的严格语法校验器（仅做语义解释）。
- 不改变 `remove_tags`、`add_tags`、`warnings`、`error` 的语义定义。

## Decisions

1) **`suggest_tags` 数据模型升级**
- 决策：将 `suggest_tags` 由 `string[]` 改为 `object[]`，对象结构为：
  - `tag: string`
  - `note: string`
- 备选方案：
  - 仅保留字符串数组并新增并行字段 `suggest_tag_notes: string[]`。
- 取舍理由：
  - 并行数组容易产生错位风险；
  - 对象结构自描述性更强，便于后续扩展（例如 `confidence`）。

2) **`tag_note_language` 作用域**
- 决策：`tag_note_language` 仅影响 `suggest_tags[].note` 的语言表达，不影响标签推断、映射、排序和其他字段。
- 备选方案：
  - 把该参数作为全局输出语言开关，影响 `warnings/error` 等文本字段。
- 取舍理由：
  - 全局语言切换会引入不必要耦合并改变已有行为；
  - 当前需求只针对 tag 含义解释，局部作用域更稳妥。

3) **排序与去重策略**
- 决策：`suggest_tags` 以 `tag` 为唯一键去重，最终按 `tag` 字典序稳定排序；同一 `tag` 出现多次时保留首个有效 `note`。
- 备选方案：
  - 以 `(tag, note)` 组合作为唯一键。
- 取舍理由：
  - 业务主键是 `tag`；同 tag 多 note 会给调用方造成冲突，不利于确定性输出。

4) **参数格式策略**
- 决策：`tag_note_language` 类型为字符串，不强制枚举或正则；文档推荐 BCP 47 命名。
- 备选方案：
  - 强制限定为 BCP 47 正则。
- 取舍理由：
  - 运行环境中语言意图可能来自自然语言；过严校验会阻断可用输入。

## Risks / Trade-offs

- [兼容性破坏：调用方仍按字符串数组读取 `suggest_tags`] → Mitigation: 在 proposal/spec/tasks 明确 **BREAKING**，并更新 schema 与示例。
- [note 内容质量不稳定] → Mitigation: 在 `SKILL.md` 强调 note 为“语义解释”且与 tag 强绑定，避免模板化空话。
- [参数误用为全局语言开关] → Mitigation: 在契约与 `SKILL.md` 同时声明参数作用域仅限 `suggest_tags[].note`。

## Migration Plan

1. 更新 change delta specs（输出结构、参数语义、排序去重规则）。
2. 更新 `SKILL.md` 与 `assets/*.schema.json`/`runner.json` 契约文档。
3. 调整规范化与校验脚本逻辑以适配对象化 `suggest_tags`。
4. 更新 fixtures/tests，覆盖新旧结构差异与参数作用域。
5. 通过 `pytest`、`mypy`、`openspec validate` 后进入 apply 阶段。

## Open Questions

- `note` 是否需要最小长度或禁止空字符串？当前阶段建议仅要求为非空语义文本，后续可在实现阶段细化。
