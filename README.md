# tag-regulator

本目录是 `$tag-regulator` 的**可发布 Agent Skill 包**。

## 文档语言规范

发布包内的文本文档（至少包含 `SKILL.md` 与 `README.md`）后续改动以中文为准；若出现中英混杂，以中文表述为权威版本。

## 发布内容（会随 skill 一起发布）

- `SKILL.md`：核心实现面（LLM 指令、强约束、流程、示例）。
- `assets/`：运行时相关文档与静态资源。
- `scripts/validate_valid_tags.py`：运行时输入校验脚本（仅允许 YAML/JSON，且必须解析为字符串数组）。
- `scripts/normalize_output.py`：运行时输出收敛脚本（去重 + 稳定排序）。

## 不发布内容（仅开发期使用）

仓库级开发产物位于本目录之外（如 `openspec/`、`references/`、仓库根 `tests/`、`dev-tools/tag-regulator/` 等）。

## 本地校验（开发用）

对一次“已捕获的 skill 输出 JSON”进行 schema 与约束校验：

```bash
conda run --no-capture-output -n DataProcessing \
  python dev-tools/tag-regulator/scripts/validate_output.py \
  --output /path/to/output.json \
  --payload /path/to/payload.json \
  --schema dev-tools/tag-regulator/assets/output_schema.json
```

对已捕获的输出 JSON 做规范化（去重 + 稳定排序），原地写回：

```bash
conda run --no-capture-output -n DataProcessing \
  python tag-regulator/scripts/normalize_output.py \
  --output /path/to/output.json
```

校验 `valid_tags` 文件合法性（运行时前置步骤）：

```bash
conda run --no-capture-output -n DataProcessing \
  python tag-regulator/scripts/validate_valid_tags.py \
  --valid-tags /path/to/valid_tags \
  --format yaml
```

运行测试与 mypy：

```bash
conda run --no-capture-output -n DataProcessing pytest -q
conda run --no-capture-output -n DataProcessing mypy tag-regulator/scripts
```

## 发布检查清单

- `tag-regulator/` 只包含可发布产物（无缓存、无无关文件）。
- `tag-regulator/SKILL.md` 明确并强调：
  - 非交互执行
  - stdout 仅允许单个 JSON 对象
  - required keys 完整，且回显 `metadata` 与 `input_tags`
  - `add_tags` 必须受 `valid_tags` 约束
- `python dev-tools/tag-regulator/scripts/validate_output.py ...` 对代表性样例可通过。
