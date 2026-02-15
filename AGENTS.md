# 项目级 AGENTS（tag-regulator / `$tag-regulator`）

本文件仅包含 **tag-regulator** skill 项目特有约定，用于补充上级/全局 `AGENTS.md`；全局通用规则不在此重复。

---

## 1. 运行形态（后台自动化）

- 本 skill 设计为后台自动化执行：运行过程中**不得询问用户做决策**。
- 任何分支/不确定性必须采用默认行为并继续执行，确保可批量运行、可重复。
- stdout **仅允许输出一个 JSON 对象**（不得夹杂日志/解释文本/多段输出）。

---

## 2. 输入约定（prompt 内 payload）

- 本 skill 以 `$tag-regulator` 被调用。
- 从 prompt 中读取：
  - `metadata`: 论文元数据，自由类型。
  - `input_tags`：待规范的tag列表，每个元素均为一个字符串。
  - `infer_tag`： 是否需要从元数据中推断tag。（布尔型，可以从prompt的语义中推断，默认true）
  - `valid_tags_format`：受控词表文件格式，枚举：`yaml|json|auto`，默认 `yaml`。`auto` 仅在显式指定时启用（按 `yaml->json` 尝试）。

- 受控tag词表 `valid_tags` 不再直接以字符串数组输入，而是通过 Skill-Runner 的 input 文件注入：
  - `{{ input.valid_tags }}`：受控词表文件路径（Runner 严格键匹配 `uploads/valid_tags` 注入为绝对路径）
  - 规范化后的tag**必须**全部在解析后的受控词表集合中。

---

## 3. 输出约定（schema 硬约束）

输出 JSON 必须包含（即使为空也要存在）：
- `remove_tags`（需要从输入tag列表中移除的tag列表，其中元素必须是 `input_tags` 中的条目）
- `add_tags`（需要新加入的tag列表，其中元素不得重复）
- `suggest_tags` （规范后得到的、或是通过推断得到的、且未在受控tag词表中的tag列表，需要符合受控tag的规范）
- `provenance.generated_at`（UTC ISO‑8601）
- `warnings`（数组）
- `error`（`object|null`）

---

## 4. 默认行为（必须遵守，不可交互询问）

- 读取 `input_tags` 或 `valid_tags` 任何一个失败（不存在/无权限/编码异常）：返回 schema 兼容 JSON，并填充 `error`；`remove_tags=[]`，`add_tags=[]`。
 - 读取 `input_tags` 失败，或读取/解析 `{{ input.valid_tags }}` 失败（缺失/不可读/编码异常/格式不符）：返回 schema 兼容 JSON，并填充 `error`；`remove_tags=[]`，`add_tags=[]`。
- `metadata` 未给出或为空时，默认 `infer_tag` 为 false，无视用户输入。
- 用户显式输入 `infer_tag` 无法解析为 “真” 或 “假” 的语义时，默认为true。

- `valid_tags_format` 未给出时默认 `yaml`。
- `valid_tags_format` 取值为 `yaml|json` 且解析失败时，不允许自动降级尝试其它格式，直接返回 `error`。

---

## 5. metadata说明

- metadata允许自由类型的输入，只要包含清晰的元数据语义即可。
- 以下形式的JSON对象可以作为合法的metadata输入：
```json
"metadata": {
  "title": "string",
  "abstract": "string",
  "authors": ["string"],
  "publication_title": "string",
  "publisher": "string",
  "institution": "string",
  "conference_name": "string",
  "keywords": ["string"],
}
```
- 以下形式的文本也可以作为合法的metadata输入：
```text
Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, and Sergey Zagoruyko. End-to-end object detection with transformers. In ECCV, 2020.
```
- 以下形式的bibtex条目也可以作为合法的metadata输入：
```bibtex
@inproceedings{carion_endtoend-object_2020,
  title = {End-to-End Object Detection with Transformers},
  booktitle = {Computer Vision -- ECCV 2020},
  author = {Carion, Nicolas and Massa, Francisco and Synnaeve, Gabriel and Usunier, Nicolas and Kirillov, Alexander and Zagoruyko, Sergey},
  year = 2020,
  pages = {213--229},
  publisher = {Springer International Publishing},
}
```
- 可用于推断 tag 的高优先级字段包括（但不限于）:
  - `title`
  - `abstract`
  - `keywords`
  - `conference_name`
  - `publication_title`  

---

## 6. 防串单对齐（必须回显）

响应必须回显：
 - `metadata`
 - `input_tags`

调用方会用它们做一致性校验；不一致将导致写回被拒绝。

## 7. 参考文档

- `references/tag_standard`: Tag维护说明，内含受控tag的规范说明。
- `references/valid_tag_list`：受控tag词表（暂行版）

## 8. 其他

skill发布目录位于 `tag-regulator/` , 发布目录中不得包含不应属于skill包的内容。
