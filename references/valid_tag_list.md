# Zotero Tag 受控词表（Controlled Vocabulary）

> 本文档只列“允许使用/推荐使用”的标准 tag（受控词表）。  
> 原则：**鼓励缩写**；核心缩写 **必须大写**；非缩写部分 **小写**。  
> `facet` 永远小写：`field:`、`topic:`、`method:`、`model:`、`status:` 等。

---

## 1) 缩写注册表（必须大写）

> 出现以下缩写时，必须使用大写形式（禁止写成小写或展开长词并存）。

### 学科体系常用缩写
- `CE` = Civil Engineering（土木工程）
- `GT` = Geotechnical Engineering（岩土）
- `UG` = Underground Engineering（地下工程）
- `CS` = Computer Science（计算机）
- `AI` = Artificial Intelligence
- `CV` = Computer Vision
- `DL` = Deep Learning
- `ML` = Machine Learning
- `MGMT` = Management / Engineering Management（管理/工程管理）
- `TBM` = Tunnel Boring Machine
- `NATM` = New Austrian Tunneling Method

### 数值方法/本构模型缩写
- `FE` = Finite Element
- `FD` = Finite Difference
- `DEM` = Discrete Element
- `MPM` = Material Point Method
- `THM` = Thermo-Hydro-Mechanical coupling
- `MC` = Mohr–Coulomb
- `HB` = Hoek–Brown
- `DP` = Drucker–Prager
- `CC` = Cam-Clay

### 风险方法缩写（如使用）
- `AHP`, `FMEA`

> 若需新增缩写：必须先在本表登记（含全称），并按《维护说明》治理流程试运行与复盘。

---

## 2) `field:` 学科体系（一级/二级/方向）

> 结构：`field:<一级>/<二级>/<方向>`  
> 每篇文献至少 1 个 `field:`（最多 2 个）。

### 2.1 土木工程（CE）
- `field:CE/GT`  
- `field:CE/GT/Rock`  
- `field:CE/GT/Soil`  
- `field:CE/GT/Ground-improvement`

- `field:CE/UG`  
- `field:CE/UG/Tunnel`  
- `field:CE/UG/TBM`  
- `field:CE/UG/NATM`  
- `field:CE/UG/Cavern`  
- `field:CE/UG/Shaft`

> 说明：`Tunnel` 已作为 `UG` 下方向；不再使用独立根节点 `field:tunneling`。

### 2.2 计算机（CS）与 AI（交叉学科）
- `field:CS/AI`
- `field:CS/AI/ML`
- `field:CS/AI/DL`
- `field:CS/AI/CV`

### 2.3 风险与管理（MGMT）
- `field:MGMT/Risk`
- `field:MGMT/Risk/Assessment`
- `field:MGMT/Risk/Management`

> 工程场景通过第二个 `field:` 交叉表达：例如 `field:MGMT/Risk/Assessment` + `field:CE/UG/Tunnel`

---

## 3) `topic:` 研究对象/问题域（半受控，可扩展）

> 0–4 个/篇；只标你会筛选的主题。  
> 非缩写一律小写，多词用 `-`。

### 3.1 隧道/地下工程对象
- `topic:lining`
- `topic:segment`
- `topic:shotcrete`
- `topic:rock-bolt`
- `topic:grouting`
- `topic:groundwater`
- `topic:face-stability`
- `topic:settlement`
- `topic:deformation`
- `topic:collapse`
- `topic:leakage`
- `topic:crack`
- `topic:durability`

### 3.2 岩土力学现象
- `topic:plastic-zone`
- `topic:damage`
- `topic:fracture`
- `topic:creep`
- `topic:soft-rock`
- `topic:squeezing`
- `topic:rockburst`
- `topic:swelling`

### 3.3 风险对象
- `topic:risk-source`
- `topic:risk-factor`
- `topic:hazard`
- `topic:uncertainty`

### 3.4 AI/CV 应用对象
- `topic:inspection`
- `topic:defect-detection`
- `topic:monitoring`
- `topic:image-based`

---

## 4) `method:` 研究方法/流程（受控为主）

### 4.1 数值/计算
- `method:numerical/simulation`
- `method:numerical/parameter-calibration`
- `method:numerical/sensitivity-analysis`
- `method:numerical/inversion`

### 4.2 实验与现场
- `method:lab-test`
- `method:field-test`
- `method:field-monitoring`

### 4.3 风险方法（非缩写小写；若用缩写必须大写）
- `method:risk/AHP`
- `method:risk/fuzzy`
- `method:risk/bayesian`
- `method:risk/FMEA`
- `method:risk/monte-carlo`
- `method:risk/fault-tree`
- `method:risk/event-tree`

### 4.4 综述
- `method:review/narrative`
- `method:review/systematic`

---

## 5) `model:` 模型/算法/本构（鼓励缩写）

> 建议 0–3 个/篇。  
> 规则：缩写必须大写；非缩写小写；DL/ML/CV 建议用路径表达族谱。

### 5.1 数值方法
- `model:FE`
- `model:FD`
- `model:DEM`
- `model:MPM`
- `model:THM`

### 5.2 本构/准则
- `model:MC`
- `model:HB`
- `model:DP`
- `model:CC`

### 5.3 ML（传统机器学习）
- `model:ML/SVM`
- `model:ML/RF`
- `model:ML/XGBoost`

### 5.4 DL（深度学习）
- `model:DL/CNN`
- `model:DL/UNet`
- `model:DL/Transformer`
- `model:DL/GNN`
- `model:DL/SSL`

### 5.5 CV 范式（可与 DL 并存）
- `model:CV/detection`
- `model:CV/segmentation`
- `model:CV/tracking`
- `model:CV/SLAM`

---

## 6) `ai_task:` AI 任务类型（固定为主）

- `ai_task:classification`
- `ai_task:regression`
- `ai_task:forecasting`
- `ai_task:detection`
- `ai_task:segmentation`
- `ai_task:pose-estimation`
- `ai_task:anomaly-detection`
- `ai_task:RL`
- `ai_task:multimodal`

> 说明：`RL` 属于缩写，必须大写。

---

## 7) `data:` 数据类型/模态（受控为主）
- `data:image`
- `data:video`
- `data:point-cloud`
- `data:timeseries`
- `data:sensor`
- `data:field-monitoring`
- `data:simulation`

---

## 8) `tool:` 工具/平台（按官方拼写/驼峰；不强制全小写）

> 工具名属于专有名词，建议使用其常见官方写法（便于辨识与统一）。

- `tool:Abaqus`
- `tool:ANSYS`
- `tool:FLAC3D`
- `tool:PLAXIS`
- `tool:COMSOL`
- `tool:Python`
- `tool:PyTorch`
- `tool:TensorFlow`

> 若你偏好更统一，也可以约定“工具全部用官方常见大写/驼峰”，禁止小写变体（如 `pytorch`）。

---

## 9) `status:` 阅读与加工状态（固定；建议彩色标签）

- `status:0-inbox`
- `status:1-triaged`
- `status:2-to-read`
- `status:3-reading`
- `status:4-annotated`
- `status:5-extracted`
- `status:6-cited`
- `status:x-parked`

---

## 10) `match_status:` 文献↔研究笔记匹配状态（固定）

- `match_status:unmatched`
- `match_status:matched`
- `match_status:partial`
- `match_status:needs-review`

---

## 11) 组合示例（速查）

### 11.1 数值仿真（隧道/岩土）
- `field:CE/UG/Tunnel`
- `field:CE/GT/Rock`
- `method:numerical/simulation`
- `model:FE`
- `model:MC`
- `tool:Abaqus`
- `status:2-to-read`
- `match_status:unmatched`

### 11.2 CV + DL（隧道病害检测）
- `field:CE/UG/Tunnel`
- `field:CS/AI/CV`
- `topic:crack`
- `ai_task:segmentation`
- `model:DL/CNN`
- `data:image`
- `tool:PyTorch`
- `status:2-to-read`
- `match_status:unmatched`

### 11.3 风险评估（隧道工程场景）
- `field:MGMT/Risk/Assessment`
- `field:CE/UG/Tunnel`
- `method:risk/bayesian`（或 `method:risk/AHP`）
- `topic:risk-factor`
- `status:2-to-read`
- `match_status:unmatched`

---

## 12) 版本记录
- v2.0：采用“缩写必须大写 + 其余小写”；`field:` 三段式并合并 UG 与 Tunnel；拆分维护说明与受控词表文档。
- v1.0: 初版发布。