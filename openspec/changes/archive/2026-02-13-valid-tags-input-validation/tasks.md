## 1. 契约与资产收敛（移除 txt 入口）

- [x] 1.1 更新 `tag-regulator/assets/parameter.schema.json`：`valid_tags_format` 仅保留 `yaml|json|auto`
- [x] 1.2 更新 `tag-regulator/assets/input.schema.json`：移除 `.txt` 扩展名提示
- [x] 1.3 更新 `AGENTS.md` 与 `tag-regulator/SKILL.md` 的格式约定，确保仅允许 YAML/JSON（`auto` 可选）

## 2. 运行时前置校验脚本

- [x] 2.1 新增 `tag-regulator/scripts/validate_valid_tags.py`，实现 YAML/JSON 解析与“顶层字符串数组”校验
- [x] 2.2 在 `tag-regulator/SKILL.md` 明确：执行开始先调用该脚本；失败直接走错误兜底
- [x] 2.3 为脚本提供无脚本回退等价规则（保持与脚本判定一致）

## 3. 开发校验与测试同步

- [x] 3.1 更新 `dev-tools/tag-regulator/scripts/validate_output.py` 的格式支持（移除 txt）
- [x] 3.2 新增/更新测试用例，覆盖 YAML/JSON 合法与非法结构、`auto` 分支行为
- [x] 3.3 运行 `conda run --no-capture-output -n DataProcessing pytest -q`
- [x] 3.4 运行 `conda run --no-capture-output -n DataProcessing mypy tag-regulator/scripts dev-tools/tag-regulator/scripts`
