#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
RAW_IDEAS_PATH = ROOT / "site/data/ideas-raw.json"
EXPANDED_DIR = ROOT / "content/ideas"
OUTPUT_DIR = ROOT / "site"
IDEA_PAGES_DIR = OUTPUT_DIR / "ideas"
DATA_OUT = OUTPUT_DIR / "data/ideas.json"


PLACEHOLDER_VISUALS = [
    {
        "title": "状态 1：任务呈现",
        "caption": "该 idea 尚未完成调研，暂以占位图示意。",
        "diagram_type": "frame",
        "asset": "assets/diagrams/placeholder-1.svg",
    },
    {
        "title": "状态 2：用户操作",
        "caption": "后续将补充真实交互步骤与视觉说明。",
        "diagram_type": "frame",
        "asset": "assets/diagrams/placeholder-2.svg",
    },
    {
        "title": "状态 3：信号判定",
        "caption": "后续将补充信号判定逻辑与可视化。",
        "diagram_type": "frame",
        "asset": "assets/diagrams/placeholder-3.svg",
    },
]


def safe_json(data) -> str:
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def load_raw_ideas() -> list[dict]:
    return json.loads(RAW_IDEAS_PATH.read_text(encoding="utf-8"))


def load_expanded_ideas() -> dict[str, dict]:
    expanded = {}
    for path in sorted(EXPANDED_DIR.glob("idea-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        expanded[data["slug"]] = data
    return expanded


def merge_idea(raw: dict, expanded: Optional[dict]) -> dict:
    base = {
        "id": raw["id"],
        "slug": raw["slug"],
        "title": raw["title"],
        "concept": raw.get("concept", ""),
        "novelty": raw.get("novelty", ""),
        "group": raw.get("group"),
        "phase": raw.get("phase"),
        "kind": raw.get("kind", "idea"),
    }
    if expanded:
        merged = {**base, **expanded}
        merged["status"] = "expanded"
        merged["summary"] = expanded.get("summary") or base["concept"]
        return merged

    base.update(
        {
            "status": "draft",
            "summary": base["concept"] or "待补充。",
            "background": base.get("novelty") or "待补充。",
            "core_mechanism": [],
            "user_flow": [],
            "signals": [],
            "decision_logic": "待补充。",
            "attack_surface": [],
            "mitigations": [],
            "accessibility": "待补充。",
            "risks": [],
            "visuals": PLACEHOLDER_VISUALS,
            "references": [],
        }
    )
    return base


def render_index(ideas: list[dict], stats: dict) -> str:
    idea_payload = [
        {
            "id": idea["id"],
            "slug": idea["slug"],
            "title": idea["title"],
            "summary": idea.get("summary", ""),
            "concept": idea.get("concept", ""),
            "group": idea.get("group"),
            "phase": idea.get("phase"),
            "kind": idea.get("kind"),
            "status": idea.get("status"),
        }
        for idea in ideas
    ]
    return f"""<!DOCTYPE html>
<html lang="zh-Hans">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>CAPTCHA 设计图谱</title>
    <link rel="stylesheet" href="assets/styles.css" />
  </head>
  <body>
    <div class="topbar">
      <div class="logo">CAPTCHA 设计图谱</div>
      <div class="badge">样例阶段 · 静态可视化</div>
    </div>
    <main>
      <section class="hero">
        <div>
          <h1>多模态时代的验证码构想</h1>
          <p>以“人类感知与动作差异”为底座，构建可视化的验证码方案目录。每个 idea 独立页面展示逻辑、信号与风险，便于评审与迭代。</p>
        </div>
        <div class="hero-panel">
          <h2>已扩展 / 全部</h2>
          <div class="stat"><span id="expanded-count">0</span> / <span id="total-count">0</span></div>
          <p id="filter-count">当前筛选：0</p>
          <p>当前为样例批次，未扩展条目以占位页标记。</p>
        </div>
      </section>

      <section class="filters">
        <input id="filter-search" type="search" placeholder="搜索标题/概念/分组" />
        <select id="filter-group"></select>
        <select id="filter-phase"></select>
        <select id="filter-kind"></select>
        <select id="filter-status"></select>
      </section>

      <section class="idea-grid" id="idea-grid"></section>
    </main>

    <script>
      window.__IDEAS__ = {safe_json(idea_payload)};
      window.__STATS__ = {safe_json(stats)};
    </script>
    <script src="assets/app.js"></script>
  </body>
</html>
"""


def render_list(items: list[str], empty_text: str = "待补充。") -> str:
    if not items:
        return f"<p>{empty_text}</p>"
    items_html = "".join(f"<li>{item}</li>" for item in items)
    return f"<ul>{items_html}</ul>"


def render_signals(signals: list[dict]) -> str:
    if not signals:
        return "<p>待补充。</p>"
    cards = []
    for signal in signals:
        cards.append(
            f"""
<div class="signal-item">
  <strong>{signal.get('signal', '')}</strong>
  <div>{signal.get('why_it_matters', '')}</div>
</div>
"""
        )
    return f"<div class=\"signal-list\">{''.join(cards)}</div>"


def render_visuals(visuals: list[dict], asset_prefix: str) -> str:
    if not visuals:
        visuals = PLACEHOLDER_VISUALS
    cards = []
    for visual in visuals:
        asset = visual.get("asset", "assets/diagrams/placeholder-1.svg")
        asset_path = asset_prefix + asset
        cards.append(
            f"""
<div class="visual-card">
  <img src="{asset_path}" alt="{visual.get('title', '')}" />
  <h3>{visual.get('title', '')}</h3>
  <p>{visual.get('caption', '')}</p>
</div>
"""
        )
    return f"<div class=\"visual-grid\">{''.join(cards)}</div>"


def render_references(references: list[dict]) -> str:
    if not references:
        return "<p>待补充。</p>"
    cards = []
    for ref in references:
        title = ref.get("title", "")
        url = ref.get("url", "")
        note = ref.get("note", "")
        cards.append(
            f"""
<div class="reference-item">
  <a href="{url}" target="_blank" rel="noreferrer">{title}</a>
  <div>{note}</div>
</div>
"""
        )
    return f"<div class=\"reference-list\">{''.join(cards)}</div>"


def render_idea_page(idea: dict) -> str:
    status_label = "已扩展" if idea.get("status") == "expanded" else "待扩展"
    status_class = "status-expanded" if idea.get("status") == "expanded" else "status-draft"
    summary = idea.get("summary", "")
    concept = idea.get("concept", "")
    novelty = idea.get("novelty", "")

    draft_note = ""
    if idea.get("status") != "expanded":
        draft_note = (
            "<section class=\"section\">"
            "<h2>提示</h2>"
            "<p>该条目尚未完成调研扩展，当前内容为原始概念占位，后续将补充细化说明与可视化。</p>"
            "</section>"
        )

    return f"""<!DOCTYPE html>
<html lang="zh-Hans">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>#{idea['id']} {idea['title']} · CAPTCHA 设计图谱</title>
    <link rel="stylesheet" href="../assets/styles.css" />
  </head>
  <body class="idea-page">
    <div class="topbar">
      <div class="logo">CAPTCHA 设计图谱</div>
      <a class="back-link" href="../index.html">← 返回索引</a>
    </div>
    <main>
      <section class="idea-hero">
        <div class="card-top">
          <span class="chip accent">#{idea['id']}</span>
          <span class="chip teal">{idea.get('group', '')}</span>
          <span class="chip blue">{status_label}</span>
        </div>
        <h1>{idea['title']}</h1>
        <p>{summary}</p>
        <div class="idea-meta">
          <span>阶段：{idea.get('phase', '')}</span>
          <span class="{status_class}">状态：{status_label}</span>
        </div>
      </section>

      {draft_note}

      <section class="section">
        <h2>概念原文</h2>
        <p>{concept}</p>
        <p>{novelty}</p>
      </section>

      <section class="section">
        <h2>研究背景</h2>
        <p>{idea.get('background', '待补充。')}</p>
      </section>

      <section class="section">
        <h2>核心机制</h2>
        {render_list(idea.get('core_mechanism', []))}
      </section>

      <section class="section">
        <h2>用户流程</h2>
        {render_list(idea.get('user_flow', []))}
      </section>

      <section class="section">
        <h2>判定信号</h2>
        {render_signals(idea.get('signals', []))}
      </section>

      <section class="section">
        <h2>判定逻辑</h2>
        <p>{idea.get('decision_logic', '待补充。')}</p>
      </section>

      <section class="section">
        <h2>对抗面</h2>
        {render_list(idea.get('attack_surface', []))}
      </section>

      <section class="section">
        <h2>防御与缓解</h2>
        {render_list(idea.get('mitigations', []))}
      </section>

      <section class="section">
        <h2>可达性与风险</h2>
        <p>{idea.get('accessibility', '待补充。')}</p>
        {render_list(idea.get('risks', []), empty_text='')}
      </section>

      <section class="section">
        <h2>可视化状态</h2>
        {render_visuals(idea.get('visuals', []), '../')}
      </section>

      <section class="section">
        <h2>参考资料</h2>
        {render_references(idea.get('references', []))}
      </section>
    </main>
  </body>
</html>
"""


def main() -> None:
    raw_ideas = load_raw_ideas()
    expanded_map = load_expanded_ideas()

    ideas = [merge_idea(raw, expanded_map.get(raw["slug"])) for raw in raw_ideas]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IDEA_PAGES_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "data").mkdir(parents=True, exist_ok=True)

    stats = {
        "total": len(raw_ideas),
        "expanded": sum(1 for idea in ideas if idea.get("status") == "expanded"),
    }

    DATA_OUT.write_text(safe_json(ideas) + "\n", encoding="utf-8")

    index_html = render_index(ideas, stats)
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    for idea in ideas:
        page_html = render_idea_page(idea)
        (IDEA_PAGES_DIR / f"{idea['slug']}.html").write_text(page_html, encoding="utf-8")


if __name__ == "__main__":
    main()
