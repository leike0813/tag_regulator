## Why

当前 `tag-regulator` 的推断证据主要来自 `metadata`，在摘要缺失或字段稀疏时会影响推断精度与 `suggest_tags[].note` 质量。Zotero-Skills workflow 已可在存在 literature digest 时提供 `digest_markdown` 文件输入，需要 skill 端无缝接入且保持向后兼容。

## What Changes

- 新增可选输入字段 `input.digest_markdown`（Markdown 文件路径），作为推断语义补充上下文。
- 保持输出 schema 与核心约束不变：单 JSON 输出、`add_tags ⊆ valid_tags`、`remove_tags ⊆ input_tags`、`suggest_tags[].tag ∉ valid_tags`。
- 在 `infer_tag=true` 且 digest 可读时，将 digest 用作 metadata 之后的补充证据；在 digest 缺失/不可读/编码异常时记录 warning 并忽略，不触发失败兜底。
- 更新 SKILL 契约与运行配置（input schema、runner prompt）以声明该可选输入。

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `tag-regulator-skill-contract`: 扩展输入 payload 契约，支持可选 `digest_markdown`，并定义“读取失败不致命”的处理规则。
- `semantic-tag-normalization-and-inference`: 扩展推断证据源优先级，定义 digest 仅作补充证据且不改变受控词表路由约束。

## Impact

- 受影响文件：`tag-regulator/assets/input.schema.json`、`tag-regulator/assets/runner.json`、`tag-regulator/SKILL.md`。
- 受影响规格：`openspec/specs/tag-regulator-skill-contract/spec.md`、`openspec/specs/semantic-tag-normalization-and-inference/spec.md`（通过本 change 的 delta specs）。
- 测试需新增输入 schema 与 runner 注入校验，并补充 SKILL 文档行为回归检查。
