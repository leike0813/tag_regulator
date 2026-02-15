## 脚本/资产分类清单

### 发布目录 `tag-regulator/`（运行时必需）

- `scripts/normalize_output.py`
  - 分类：运行时必需
  - 用途：最终输出前进行去重与稳定排序收敛
  - 说明：在 `SKILL.md` 中已定义调用时机与失败回退

### 迁出到开发工具目录 `dev-tools/tag-regulator/`（开发期专用）

- `scripts/validate_output.py`
  - 分类：开发期专用
  - 用途：schema + 业务约束校验（测试/CI/离线验收）
- `scripts/cli.py`
  - 分类：开发期专用
  - 用途：统一本地开发命令入口（validate/normalize）
- `assets/output_schema.json`
  - 分类：开发期专用
  - 用途：校验输出结构（与 validate 脚本配套）

## 迁移映射

- `tag-regulator/scripts/validate_output.py` → `dev-tools/tag-regulator/scripts/validate_output.py`
- `tag-regulator/scripts/cli.py` → `dev-tools/tag-regulator/scripts/cli.py`
- `tag-regulator/assets/output_schema.json` → `dev-tools/tag-regulator/assets/output_schema.json`
