## 1. OpenSpec 契约与工件

- [x] 1.1 完成 `proposal.md`：声明 `digest_markdown` 为可选输入与非目标边界
- [x] 1.2 完成 delta specs：更新 `tag-regulator-skill-contract` 与 `semantic-tag-normalization-and-inference`
- [x] 1.3 完成 `design.md`：固化 digest 读取失败策略与推断优先级

## 2. 输入接口与文档实现

- [x] 2.1 更新 `tag-regulator/assets/input.schema.json`：新增可选 `digest_markdown` 文件输入定义（Markdown 扩展名）
- [x] 2.2 更新 `tag-regulator/assets/runner.json`：在 prompt 中注入 `digest_markdown={{ input.digest_markdown }}`
- [x] 2.3 更新 `tag-regulator/SKILL.md`：新增 payload 字段与 Step 0/Step 3 的 digest 读取与优先级说明

## 3. 测试与回归

- [x] 3.1 新增/更新测试与 fixtures：覆盖无 digest、有 digest、digest 路径不可用时的契约行为
- [x] 3.2 运行 `conda run --no-capture-output -n DataProcessing pytest -q`
- [x] 3.3 运行 `conda run --no-capture-output -n DataProcessing mypy tag-regulator/scripts dev-tools/tag-regulator/scripts`
- [x] 3.4 运行 `openspec validate --type change support-digest-markdown-input --strict --json`
