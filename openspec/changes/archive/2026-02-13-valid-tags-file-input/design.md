## Context

当前 `$tag-regulator` 约定 `valid_tags` 作为 payload 中的字符串数组输入，但在真实应用中受控词表体量可能很大，将其展开到 prompt 中既麻烦也容易导致超长。与此同时，Skill-Runner 的 Strict Key-Matching 机制要求上传文件名与 input schema 字段名完全一致（例如 `uploads/valid_tags`），这会导致文件缺少扩展名，进而增加格式猜测负担。

本次变更将 `valid_tags` 改为 Runner `input.valid_tags` 注入的文件路径，并新增 `valid_tags_format` 参数来显式指定文件内容格式，默认 `yaml`，可选 `auto` 且仅在用户显式指定时启用。

## Goals / Non-Goals

**Goals:**
- `valid_tags` 改为文件输入（`{{ input.valid_tags }}` 为路径），不再从 payload 传入数组。
- 引入 `valid_tags_format` 参数（默认 `yaml`，支持 `yaml|json|txt|auto`），避免隐式格式猜测。
- 在不改变现有 tag 规范化与推断语义的前提下，保持输出契约与失败兜底一致。
- 增补 Runner 所需的 schema/runner 声明文件，允许上传 `uploads/valid_tags` 被注入为路径。

**Non-Goals:**
- 不将 `input_tags`/`metadata` 一并改为文件输入（本次只聚焦 `valid_tags`）。
- 不在 `valid_tags_format` 指定失败后进行隐式“自动降级尝试其它格式”（避免误解析）。

## Decisions

1) **输入拆分：payload vs runner input**
- payload 继续承载：`metadata`、`input_tags`、`infer_tag`。
- runner input 承载：`valid_tags` 文件路径（通过 `{{ input.valid_tags }}`）。

2) **格式参数：`valid_tags_format`**
- 默认：`yaml`。
- 可选：`json`、`txt`、`auto`。
- `auto` 仅在用户显式指定时启用；启用后按 `yaml -> json -> txt` 的顺序尝试解析。
- 当 `valid_tags_format` 指定为 `yaml|json|txt` 时，解析失败直接进入错误兜底，不再尝试其它格式。

3) **支持的文件内容约定**
- `yaml`：顶层为字符串列表（每项是一个 tag）。
- `json`：顶层为字符串数组。
- `txt`：每行一个 tag，忽略空行（可选忽略前后空白）。

4) **错误兜底保持一致**
- 若读取/解析 `input.valid_tags` 失败（缺失、不可读、格式不符、类型不对），返回 schema 兼容 JSON：
  - `remove_tags=[]`，`add_tags=[]`
  - `error` 非空（至少包含 `type`、`message`）
  - 仍回显 `metadata` 与 `input_tags`（若可用）

5) **Runner 文件与 schema**
- 新增 `tag-regulator/assets/input.schema.json`：声明 `valid_tags` 为 input 文件字段（无扩展名依赖）。
- 新增 `tag-regulator/assets/parameter.schema.json`：声明 `valid_tags_format` 参数与默认值。
- 新增 `tag-regulator/assets/output.schema.json`：声明 stdout JSON 的结构（与现有输出契约一致）。
- 新增 `tag-regulator/assets/runner.json`：连接 schema 并提供执行入口 prompt（构造 payload 与 `{{ input.valid_tags }}` 注入方式）。

## Risks / Trade-offs

- [Runner 注入的文件无扩展名导致误判] → Mitigation: 使用 `valid_tags_format` 参数显式指定，默认 `yaml`。
- [auto 探测误解析] → Mitigation: 仅在用户显式指定 `auto` 时启用；并在 `warnings` 中记录使用了 auto 与最终判定格式。
- [变更破坏旧调用方] → Mitigation: 这是明确的 BREAKING 变更，在文档与 specs 中明确，调用方需要改为上传 `uploads/valid_tags` 并传入 `valid_tags_format`。
