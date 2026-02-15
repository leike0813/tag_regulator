## Context

`$tag-regulator` 的核心约束是：`add_tags` 必须完全受控于 `valid_tags`。因此 `valid_tags` 一旦被误解析，会直接影响最终写回结果。此前流程允许 `txt` 入口，虽然易用，但在文件损坏/半结构化内容场景下容易误判为“可用词表”，风险不可接受。

本次变更将入口收敛到结构化格式（YAML/JSON），并在流程起点引入确定性校验脚本，保证后续语义规范化只在“已验证词表”上执行。

## Goals / Non-Goals

**Goals**
- 在运行时提供一个轻量、确定性的 `valid_tags` 校验脚本。
- 明确脚本调用时机：执行开始即调用，失败直接走错误兜底。
- 从契约与资产层面移除 `txt` 输入入口，避免回退到弱约束解析。
- 为校验路径补充自动化测试。

**Non-Goals**
- 不改变 tag 语义推断策略与映射规则。
- 不新增复杂编排机制（仅新增前置校验步骤）。
- 不改动输出 JSON 主体契约（required keys 与 echo 规则保持不变）。

## Decisions

1) **输入格式白名单**
- `valid_tags_format` 仅允许：`yaml | json | auto`。
- 默认值仍为 `yaml`。
- `auto` 仅在显式指定时启用，按 `yaml -> json` 尝试。
- 当显式指定 `yaml` 或 `json` 且解析失败时，禁止降级尝试其它格式。

2) **校验脚本职责边界**
- 新增 `tag-regulator/scripts/validate_valid_tags.py`，唯一职责：
  - 读取 `valid_tags` 文件；
  - 按指定格式解析；
  - 断言解析结果为“顶层字符串数组”。
- 脚本不参与语义推断、不修改业务决策。

3) **SKILL 执行顺序**
- 在 `Step 0`（读取 payload）阶段先调用校验脚本。
- 校验成功后才进入后续语义流程。
- 校验失败时直接返回契约兼容错误 JSON（`remove_tags=[]`, `add_tags=[]`, `error!=null`）。
- 若运行环境无法调用脚本，执行与脚本等价的内建回退校验逻辑（同样只允许 YAML/JSON）。

4) **资产与开发工具一致性**
- 更新 `tag-regulator/assets/parameter.schema.json` 枚举，移除 `txt`。
- 更新 `tag-regulator/assets/input.schema.json` 扩展名提示，移除 `.txt`。
- 同步更新 `AGENTS.md` 与开发校验工具（`dev-tools/tag-regulator/scripts/validate_output.py`）对格式枚举的支持，避免文档与实现分叉。

## Risks / Trade-offs

- **风险：`auto` 模式下 YAML 解析器会接受 JSON**
  - 取舍：这是可接受行为；目标是“结构化且确定”，不是“区分文件扩展名来源”。
- **风险：多一步脚本调用增加运行复杂度**
  - 缓解：脚本仅做 I/O + 解析 + 类型断言，开销低；并提供无脚本回退。

## Migration Plan

1. 新增校验脚本与单元测试。
2. 更新 `SKILL.md`，明确“起始校验”与失败处理。
3. 更新 schema 与项目契约文档，去除 `txt`。
4. 运行 `pytest` 与 `mypy` 完成回归验证。

## Open Questions

- None.
