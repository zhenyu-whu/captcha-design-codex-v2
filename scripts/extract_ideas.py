#!/usr/bin/env python3
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "_bmad-output/brainstorming/brainstorming-session-2026-01-27T11-05-32.md"
DEFAULT_OUTPUT = ROOT / "site/data/ideas-raw.json"


CATEGORY_RE = re.compile(r"^\*\*\[Category\s+#(?P<id>[^\]]+)\]\*\*:\s*(?P<title>.+)$")
CONCEPT_RE = re.compile(r"^_Concept_:\s*(?P<text>.*)$")
NOVELTY_RE = re.compile(r"^_Novelty_:\s*(?P<text>.*)$")
H2_RE = re.compile(r"^##\s+(?P<text>.+)$")
H3_RE = re.compile(r"^###\s+(?P<text>.+)$")
H4_RE = re.compile(r"^####\s+(?P<text>.+)$")
BATCH_RE = re.compile(r"^\*\*批次\s*(?P<text>.+)\*\*$")


def idea_slug(raw_id: str) -> str:
    if raw_id.isdigit():
        return f"idea-{int(raw_id):03d}"
    return f"idea-{raw_id.lower()}"


def parse_ideas(md_text: str) -> list[dict]:
    ideas = []
    current_h2 = None
    current_h3 = None
    current_h4 = None
    current_batch = None
    current = None
    current_field = None

    for raw_line in md_text.splitlines():
        line = raw_line.strip()
        if not line:
            current_field = None
            continue

        h2_match = H2_RE.match(line)
        if h2_match:
            current_h2 = h2_match.group("text")
            current_h3 = None
            current_h4 = None
            current_batch = None
            continue

        h3_match = H3_RE.match(line)
        if h3_match:
            current_h3 = h3_match.group("text")
            current_h4 = None
            current_batch = None
            continue

        h4_match = H4_RE.match(line)
        if h4_match:
            current_h4 = h4_match.group("text")
            current_batch = None
            continue

        batch_match = BATCH_RE.match(line)
        if batch_match:
            current_batch = batch_match.group("text").strip()
            continue

        category_match = CATEGORY_RE.match(line)
        if category_match:
            raw_id = category_match.group("id")
            current = {
                "id": raw_id,
                "slug": idea_slug(raw_id),
                "title": category_match.group("title").strip(),
                "concept": "",
                "novelty": "",
                "phase": current_h2,
                "section": current_h3,
                "group": current_h4 or current_batch or current_h3 or current_h2,
                "batch": current_batch,
                "kind": "principle" if raw_id.upper().startswith("P") else "idea",
            }
            ideas.append(current)
            current_field = None
            continue

        if current is None:
            continue

        concept_match = CONCEPT_RE.match(line)
        if concept_match:
            current["concept"] = concept_match.group("text").strip()
            current_field = "concept"
            continue

        novelty_match = NOVELTY_RE.match(line)
        if novelty_match:
            current["novelty"] = novelty_match.group("text").strip()
            current_field = "novelty"
            continue

        if current_field in {"concept", "novelty"}:
            # 合并意外换行的说明文本
            current[current_field] = (current[current_field] + " " + line).strip()

    return ideas


def main() -> None:
    md_text = DEFAULT_INPUT.read_text(encoding="utf-8")
    ideas = parse_ideas(md_text)
    DEFAULT_OUTPUT.write_text(
        json.dumps(ideas, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
