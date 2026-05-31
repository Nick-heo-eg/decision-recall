"""Stop hook — auto-capture decision-recall markers from Claude's last response.

═══════════════════════════════════════════════════════════════════════
DECISION RECALL — self-contained Stop hook
═══════════════════════════════════════════════════════════════════════

What it does:
  Every time Claude finishes a response, scan the message body for markers
  matching one of:
    결정 / decision: <topic> | <one-line content>
    판단 / analysis: <topic> | <one-line content>
    원칙 / principle: <topic> | <one-line content>

  Each match is appended to a local JSONL trace file. No network, no
  external dependencies, no LLM calls. Pure regex + file append.

Where it appends:
  Tries (in order, first writable wins):
    1. $DECISION_RECALL_TRACE (env override)
    2. ~/decision-recall/state/recall_trace.jsonl
    3. ./state/recall_trace.jsonl (cwd-relative)

Format of each entry (one JSON object per line):
  {
    "trace_id":  "<8-char hex>",
    "timestamp": "<ISO 8601 with tz>",
    "type":      "decision" | "analysis" | "principle",
    "topic":     "<topic-slug>",
    "content":   "<one-line content>",
    "source":    "auto"          ← hook-captured (vs "live" for manual)
  }

Rules (constants below):
  - content < 10 chars  → skipped (anti-noise)
  - max 5 markers/turn  → over-marking signal, only first 5 saved
  - dedup by exact (type, topic, content) against last 50 entries
  - fail silent — never block Claude, never raise

Privacy:
  This hook never reads, transmits, or stores anything from outside the
  last assistant message text. The trace file is local-only.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

MARKER_TYPE = {
    "결정": "decision",
    "판단": "analysis",
    "원칙": "principle",
    "decision": "decision",
    "analysis": "analysis",
    "principle": "principle",
}

MARKER_RE = re.compile(
    r"^\s*(결정|판단|원칙|decision|analysis|principle)\s*[/／]?\s*(?:결정|판단|원칙|decision|analysis|principle)?\s*:\s*([^\|]+?)\s*\|\s*(.+?)\s*$",
    re.MULTILINE | re.IGNORECASE,
)

MIN_CONTENT_LEN = 10
MAX_MARKERS_PER_TURN = 5
DEDUP_WINDOW = 50


def trace_path() -> Path:
    env = os.environ.get("DECISION_RECALL_TRACE")
    if env:
        return Path(env).expanduser()
    home = Path.home() / "decision-recall" / "state" / "recall_trace.jsonl"
    if home.parent.parent.exists():
        return home
    return Path.cwd() / "state" / "recall_trace.jsonl"


def load_recent(path: Path, n: int = DEDUP_WINDOW) -> list[dict]:
    if not path.exists():
        return []
    try:
        lines = path.read_text().splitlines()[-n:]
    except Exception:
        return []
    out: list[dict] = []
    for line in lines:
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out


def is_duplicate(entry: dict, recent: list[dict]) -> bool:
    key = (entry["type"], entry["topic"], entry["content"])
    return any((r.get("type"), r.get("topic"), r.get("content")) == key for r in recent)


def make_entry(marker_token: str, topic_raw: str, content: str) -> dict:
    type_kind = MARKER_TYPE.get(marker_token.lower(), "analysis")
    topic = topic_raw.strip().lower().replace(" ", "-")
    ts = datetime.now(tz=timezone.utc).astimezone().isoformat()
    trace_id = hashlib.md5(f"{ts}|{topic}|{content}".encode()).hexdigest()[:8]
    return {
        "trace_id": trace_id,
        "timestamp": ts,
        "type": type_kind,
        "topic": topic,
        "content": content.strip(),
        "source": "auto",
    }


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    text = data.get("last_assistant_message", "")
    if not text or len(text) > 50000:
        return 0

    matches = MARKER_RE.findall(text)
    if not matches:
        return 0

    path = trace_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        return 0

    recent = load_recent(path)
    appended = 0
    seen_types: set[str] = set()

    for marker_token, topic_raw, content in matches[:MAX_MARKERS_PER_TURN]:
        content_clean = content.strip()
        if len(content_clean) < MIN_CONTENT_LEN:
            continue
        entry = make_entry(marker_token, topic_raw, content_clean)
        if is_duplicate(entry, recent):
            continue
        try:
            with path.open("a") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            appended += 1
            seen_types.add(entry["type"])
            recent.append(entry)
        except Exception:
            continue

    if appended > 0:
        types_str = ",".join(sorted(seen_types))
        print(
            f"[decision-recall] captured {appended} marker(s) [{types_str}] → {path}",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
