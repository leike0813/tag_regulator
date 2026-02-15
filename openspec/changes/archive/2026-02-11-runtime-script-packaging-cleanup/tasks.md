## 1. 脚本分类与目录治理

- [x] 1.1 审计 `tag-regulator/` 内脚本与资产，按“运行时必需/开发期专用”完成分类清单
- [x] 1.2 在仓库创建开发工具目录（`dev-tools/tag-regulator/`）并规划迁移目标路径
- [x] 1.3 将开发期专用文件迁出发布目录（`validate_output.py`、`cli.py`、`output_schema.json`）
- [x] 1.4 清理发布目录中的缓存与无关文件（例如 `__pycache__`），确保仅保留发布必需内容

## 2. 保留脚本调用契约

- [x] 2.1 保留 `tag-regulator/scripts/normalize_output.py` 作为运行时输出收敛脚本，并确认输入输出接口
- [x] 2.2 在 `tag-regulator/SKILL.md` 增加“脚本调用时机”段落（候选 JSON 生成后、最终输出前）
- [x] 2.3 在 `tag-regulator/SKILL.md` 增加“无脚本回退流程”段落（脚本不可用时手工执行等价规则）
- [x] 2.4 校验文档描述与现有输出契约一致（单 JSON 输出、required keys、约束不变）

## 3. 迁移后路径修复与验证

- [x] 3.1 更新 `tag-regulator/README.md` 中本地校验命令到迁移后路径
- [x] 3.2 更新测试文件的导入/路径引用，确保使用迁移后脚本与 schema 位置
- [x] 3.3 运行 `conda run --no-capture-output -n DataProcessing pytest -q` 验证回归
- [x] 3.4 运行 `conda run --no-capture-output -n DataProcessing mypy tag-regulator/scripts` 验证类型检查
