## 1. 契约与 Schema 更新

- [x] 1.1 更新 `tag-regulator/assets/output.schema.json`：将 `suggest_tags` 从字符串数组改为对象数组（必含 `tag`、`note`）
- [x] 1.2 更新 `tag-regulator/assets/parameter.schema.json`：新增 `tag_note_language` 字符串参数说明（推荐 BCP 47）
- [x] 1.3 更新 `tag-regulator/assets/runner.json`：将 `tag_note_language` 注入 prompt 参数上下文

## 2. SKILL 文档与运行时约束

- [x] 2.1 更新 `tag-regulator/SKILL.md`：重写 `suggest_tags` 字段定义与示例输出结构
- [x] 2.2 更新 `tag-regulator/SKILL.md`：新增 `tag_note_language` 说明并强调其仅影响 `suggest_tags[].note`
- [x] 2.3 更新 `tag-regulator/SKILL.md`：明确对象化 `suggest_tags` 的去重/稳定排序规则与无脚本回退规则

## 3. 脚本与开发校验适配

- [x] 3.1 更新 `tag-regulator/scripts/normalize_output.py`：支持对象化 `suggest_tags` 的按 `tag` 去重与稳定排序
- [x] 3.2 更新 `dev-tools/tag-regulator/scripts/validate_output.py`：支持校验 `suggest_tags[].tag` / `suggest_tags[].note` 结构与约束
- [x] 3.3 若需要，补充或更新辅助校验逻辑，确保 `tag_note_language` 作用域不外溢

## 4. 测试与回归验证

- [x] 4.1 更新/新增 fixtures：覆盖对象化 `suggest_tags` 的有效与无效样例
- [x] 4.2 更新/新增测试用例：覆盖去重、排序、结构校验与 `tag_note_language` 行为
- [x] 4.3 运行 `conda run --no-capture-output -n DataProcessing pytest -q`
- [x] 4.4 运行 `conda run --no-capture-output -n DataProcessing mypy tag-regulator/scripts dev-tools/tag-regulator/scripts`
