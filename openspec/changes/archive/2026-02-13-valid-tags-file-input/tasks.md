## 1. Runner 输入与参数声明

- [x] 1.1 新增 `tag-regulator/assets/input.schema.json`，声明 `valid_tags` 为必需 input 文件字段
- [x] 1.2 新增 `tag-regulator/assets/parameter.schema.json`，新增参数 `valid_tags_format`（默认 `yaml`，枚举含 `yaml|json|txt|auto`）
- [x] 1.3 新增 `tag-regulator/assets/output.schema.json`，描述 stdout JSON 输出结构（required keys + echo fields）
- [x] 1.4 新增 `tag-regulator/assets/runner.json`，关联 schemas 并约定 prompt 注入（使用 `{{ input.valid_tags }}` 与 `{{ parameter.valid_tags_format }}`）

## 2. 文档与契约更新

- [x] 2.1 更新 `AGENTS.md`：`valid_tags` 改为文件输入，并新增 `valid_tags_format` 规则与失败兜底
- [x] 2.2 更新 `tag-regulator/SKILL.md`：`valid_tags` 改为文件路径输入，按 `valid_tags_format` 解析（默认 yaml；auto 显式才启用；无隐式降级）
- [x] 2.3 更新 `tag-regulator/SKILL.md` 示例：用 `uploads/valid_tags` + `valid_tags_format` 替代 payload 内 `valid_tags` 数组

## 3. 开发工具与测试

- [x] 3.1 更新 `dev-tools/tag-regulator/scripts/validate_output.py`：支持通过 `--valid-tags-file`（配合 `--valid-tags-format`）提供受控词表以做约束校验
- [x] 3.2 新增测试 fixtures：`tests/fixtures/valid_tags.yaml`（小词表）与对应 payload fixture（不再内嵌 valid_tags 数组）
- [x] 3.3 更新 `tests/test_validate_output.py`：改为读取 `valid_tags.yaml` 并通过 dev-tools 解析后进行校验

## 4. 回归验证

- [x] 4.1 运行 `conda run --no-capture-output -n DataProcessing pytest -q`
- [x] 4.2 运行 `conda run --no-capture-output -n DataProcessing mypy tag-regulator/scripts dev-tools/tag-regulator/scripts`
