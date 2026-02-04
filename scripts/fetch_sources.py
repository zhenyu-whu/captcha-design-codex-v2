#!/usr/bin/env python3
import json
import re
import time
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "research/source-index.json"

SOURCES = [
    {"slug": "physiological-tremor", "url": "https://en.wikipedia.org/wiki/Physiological_tremor"},
    {"slug": "behavioral-biometrics", "url": "https://en.wikipedia.org/wiki/Behavioral_biometrics"},
    {"slug": "motor-control", "url": "https://en.wikipedia.org/wiki/Motor_control"},
    {"slug": "motor-adaptation", "url": "https://en.wikipedia.org/wiki/Motor_adaptation"},
    {"slug": "motor-learning", "url": "https://en.wikipedia.org/wiki/Motor_learning"},
    {"slug": "time-perception", "url": "https://en.wikipedia.org/wiki/Time_perception"},
    {"slug": "reaction-time", "url": "https://en.wikipedia.org/wiki/Reaction_time"},
    {"slug": "bimanual-coordination", "url": "https://en.wikipedia.org/wiki/Bimanual_coordination"},
    {"slug": "hand-eye-coordination", "url": "https://en.wikipedia.org/wiki/Hand%E2%80%93eye_coordination"},
    {"slug": "reflex", "url": "https://en.wikipedia.org/wiki/Reflex"},
    {"slug": "motor-variability", "url": "https://en.wikipedia.org/wiki/Motor_variability"},
    {"slug": "signal-processing", "url": "https://en.wikipedia.org/wiki/Signal_processing"},
    {"slug": "human-factors", "url": "https://en.wikipedia.org/wiki/Human_factors_and_ergonomics"},
    {"slug": "feedback-control", "url": "https://en.wikipedia.org/wiki/Control_theory"},
    {"slug": "latency", "url": "https://en.wikipedia.org/wiki/Latency_(engineering)"},
    {"slug": "fitts-law", "url": "https://en.wikipedia.org/wiki/Fitts%27s_law"},
    {"slug": "amodal-perception", "url": "https://en.wikipedia.org/wiki/Amodal_perception"},
    {"slug": "flicker-fusion-threshold", "url": "https://en.wikipedia.org/wiki/Flicker_fusion_threshold"},
    {"slug": "kinetic-scrolling", "url": "https://en.wikipedia.org/wiki/Kinetic_scrolling"},
    {"slug": "canvas-fingerprinting", "url": "https://en.wikipedia.org/wiki/Canvas_fingerprinting"},
    {"slug": "device-fingerprint", "url": "https://en.wikipedia.org/wiki/Device_fingerprint"},
    {"slug": "subpixel-rendering", "url": "https://en.wikipedia.org/wiki/Subpixel_rendering"},
]


TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def fetch_title(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=20) as response:
        html = response.read().decode("utf-8", errors="ignore")
    match = TITLE_RE.search(html)
    if not match:
        return ""
    return match.group(1).strip()


def main() -> None:
    results = []
    fetched_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for source in SOURCES:
        title = ""
        error = ""
        try:
            title = fetch_title(source["url"])
        except Exception as exc:  # noqa: BLE001
            error = str(exc)
        results.append(
            {
                "slug": source["slug"],
                "url": source["url"],
                "title": title,
                "error": error,
                "fetched_at": fetched_at,
            }
        )
    OUTPUT.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
