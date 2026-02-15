## 1. 文档中文化

- [x] 1.1 将 `tag-regulator/SKILL.md` 翻译为中文（保留字段名/路径/命令/JSON 结构不变）
- [x] 1.2 将 `tag-regulator/README.md` 翻译为中文（保留命令行示例不变）

## 2. 语言规范落地

- [x] 2.1 在 `tag-regulator/SKILL.md` 增加“文档语言规范”段落（后续文档改动以中文为准）
- [x] 2.2 在 `tag-regulator/README.md` 增加同样的语言规范说明（与 SKILL.md 一致）

## 3. 校验与回归

- [x] 3.1 检查中文化后内容不引入契约变化（required keys、默认行为、约束描述保持等价）
- [x] 3.2 运行 `conda run --no-capture-output -n DataProcessing pytest -q` 确认测试通过
