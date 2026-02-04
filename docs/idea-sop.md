# CAPTCHA Idea 扩展与可视化 SOP

本文档用于将任意 idea 从原始概念扩展为可评审的独立页面，并更新索引页与可视化资源。

## 1. 目的与输出

- 目的：为每个 idea 生成结构化说明与静态可视化，便于评审与后续迭代。
- 输出：
  - 扩展内容：`content/ideas/idea-XXX.json`
  - 可视化图：`site/assets/diagrams/idea-XXX-1.svg` 等
  - 生成页面：`site/ideas/idea-XXX.html`（由脚本自动生成）

## 2. 输入与依赖

- 原始想法库：`site/data/ideas-raw.json`
  - 若原始文档更新，需先运行：`python3 scripts/extract_ideas.py`
- 扩展模板：`content/idea-template.json`
- 站点构建脚本：`python3 scripts/build_site.py`

## 3. 命名规范

- 数字 idea：
  - slug：`idea-XXX`（3 位数补零，例如 `idea-002`）
  - 文件：`content/ideas/idea-002.json`
  - 页面：`site/ideas/idea-002.html`
  - 图示：`site/assets/diagrams/idea-002-1.svg` / `idea-002-2.svg` / `idea-002-3.svg`
- 原则类 idea（P1/P2）：
  - slug：`idea-p1` / `idea-p2`
  - 文件：`content/ideas/idea-p1.json`

## 4. 标准流程

### Step 0：选择与核对
1) 选择待扩展 idea（建议按分组批次推进）。
2) 在 `site/data/ideas-raw.json` 中确认：`id`、`title`、`group`、`phase` 是否正确。

### Step 1：研究与素材整理
1) 快速检索该 idea 的理论依据或研究基础。
2) 将核心参考链接整理进 `references` 字段。
3) 可选：同步记录到 `research/sources.md` 便于团队查阅。

### Step 2：扩展内容编写
1) 复制 `content/idea-template.json` 为 `content/ideas/idea-XXX.json`。
2) 按字段逐项填写：
   - `summary`：一句话说明核心验证逻辑
   - `background`：研究背景与合理性说明
   - `core_mechanism`：3–5 条机制要点
   - `user_flow`：清晰的 3–4 步操作流程
   - `signals`：2–4 个核心信号及其意义
   - `decision_logic`：判定逻辑与规则
   - `attack_surface` / `mitigations`：对抗面与缓解策略
   - `accessibility` / `risks`：可达性与潜在风险
3) 保持与原始概念一致，不要改变 `id` / `slug` / `title`。

### Step 3：可视化图示
为每个 idea 输出 3 张静态图：
1) 状态 1：任务呈现
2) 状态 2：用户操作
3) 状态 3：信号判定

图示建议规范：
- 使用统一画布：`480x300`，背景浅色
- 配色建议（与站点风格一致）：
  - 主色：`#E07B55` `#2F6F65` `#3B5B7A`
  - 背景：`#FFF9F2` `#FFFDF9`
  - 边框：`#D7C9BB` `#E1D4C8`
- 图中元素尽量抽象化，避免细节过度写实

### Step 4：构建页面
运行站点构建脚本：
```
python3 scripts/build_site.py
```

输出：
- `site/index.html`
- `site/ideas/idea-XXX.html`
- `site/data/ideas.json`

### Step 5：自检
检查以下要点：
- 索引页能正确筛选、搜索，状态显示为“已扩展”
- 详情页内容完整且逻辑清晰
- 三张图能正常显示且与描述一致
- 引用链接可访问且与内容匹配

## 5. 质量标准（快速检查）

- 结构完整：所有核心字段都有有效内容
- 逻辑一致：`summary` 与 `core_mechanism`/`signals`/`decision_logic` 一致
- 可信支撑：至少 1–2 条引用来源
- 可达性考虑：明确替代通道或负担控制
- 视觉清晰：图示能体现任务与信号，不只是装饰

## 6. 常见问题

- 为什么索引页仍显示“待扩展”？
  - 检查 `content/ideas/idea-XXX.json` 是否存在且 `slug` 正确，然后重新运行 `python3 scripts/build_site.py`。

- 想修正文档中的“概念原文”？
  - 该部分来自 `site/data/ideas-raw.json`，需修改原始 brainstorming 文档并运行 `python3 scripts/extract_ideas.py`。

- 图示不显示？
  - 检查 `visuals[].asset` 路径与 `site/assets/diagrams/` 文件是否一致。

