## Why

`valid_tags` 作为受控词表在真实使用中规模可能很大，将其以字符串数组直接嵌入 prompt payload 会造成使用繁琐、容易超长、也不利于复用与版本化。需要将 `valid_tags` 改为文件输入，并通过显式参数指定文件格式，降低 agent 的格式猜测负担并提高稳定性。

## What Changes

- **BREAKING**: `valid_tags` 不再以字符串数组形式从 payload 传入；改为通过 Skill-Runner `input.valid_tags` 传入文件路径，并在执行时读取解析。
- 新增参数 `valid_tags_format`：
  - 取值：`yaml|json|txt|auto`
  - 默认：`yaml`
  - `auto` 仅在用户显式指定时启用；不做“解析失败后自动降级尝试其它格式”的隐式行为。
- 支持的文件内容格式（以 `valid_tags_format` 为准）：
  - `yaml`：顶层为字符串列表（推荐）
  - `json`：顶层为字符串数组
  - `txt`：纯文本，每行一个 tag（忽略空行）
- 失败兜底扩展：
  - 读取/解析 `input.valid_tags` 文件失败（缺失、不可读、格式不符）时，仍按既有约束返回 schema 兼容 JSON，并填充 `error`，且 `remove_tags=[]`、`add_tags=[]`。
- 为 Runner 增补必要的 schema/runner 声明，使 `uploads/valid_tags` 可被注入为 `{{ input.valid_tags }}`，并使 `valid_tags_format` 可作为 parameter 注入。

## Capabilities

### New Capabilities

<!-- None (interface change within existing capabilities). -->

### Modified Capabilities

- `tag-regulator-skill-contract`: 调整受控词表输入接口（从 payload 数组改为 input 文件）并增加 `valid_tags_format` 参数契约与失败兜底。
- `semantic-tag-normalization-and-inference`: 受控词表来源变化（读取并解析文件得到 `valid_tags` 集合），其余规范化/推断约束不变。

## Impact

- 影响文档与接口：
  - `AGENTS.md` 与 `tag-regulator/SKILL.md` 需要更新输入约定与示例。
  - Runner 侧需要 `assets/input.schema.json`、`assets/parameter.schema.json`、`assets/runner.json`（以及必要时的 `assets/output.schema.json`）来声明文件输入与参数。
- 影响测试与开发工具：
  - 现有测试/校验如果依赖 payload 内 `valid_tags`，需要改为使用词表文件 fixture 或显式传入词表文件路径。
