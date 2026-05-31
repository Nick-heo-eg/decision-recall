"""Stop hook — auto-capture decision-recall markers from Claude's last response.

═══════════════════════════════════════════════════════════════════════
DECISION RECALL — self-contained Stop hook
═══════════════════════════════════════════════════════════════════════

What it does:
  Every time Claude finishes a response, this Stop hook reads the session
  transcript, extracts the last assistant message, and scans it for markers:
    결정 / decision: <topic> | <one-line content>
    판단 / analysis: <topic> | <one-line content>
    원칙 / principle: <topic> | <one-line content>

  Each match is appended to a single canonical JSONL trace file.

Trace file location (resolved in this order):
  1. $DECISION_RECALL_TRACE (env override)
  2. ~/decision-recall/state/recall_trace.jsonl  ← canonical default

  Note: cwd-relative fallback is intentionally NOT used. In a multi-project
  workflow the trace must live in one place, not split per project.

Input contract (Claude Code Stop hook):
  stdin = JSON with:
    - transcript_path: absolute path to session .jsonl
    - cwd, session_id, hook_event_name, stop_hook_active

  We open transcript_path, scan from the end for the last entry whose
  message.role == "assistant", and use that message's text as the source.

  (Older hook spec used a `last_assistant_message` field directly in stdin.
  We support it as a fallback in case the runtime still provides it.)

Rules:
  - content < 10 chars  → skipped (anti-noise)
  - max 5 markers/turn  → over-marking signal, only first 5 saved
  - dedup by exact (type, topic, content) against last 50 entries
  - stop_hook_active == True → exit immediately (avoid recursion)
  - fail silent — never block Claude, never raise

Privacy:
  This hook never reads files outside the transcript Claude itself passed
  to us. Trace file is local-only.
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
    r"^[\s\-\*•]*(결정|판단|원칙|decision|analysis|principle)\s*[/／]?\s*(?:결정|판단|원칙|decision|analysis|principle)?\s*:\s*([^\|]+?)\s*\|\s*(.+?)\s*$",
    re.MULTILINE | re.IGNORECASE,
)

MIN_CONTENT_LEN = 10
MAX_MARKERS_PER_TURN = 5
DEDUP_WINDOW = 50


def trace_path() -> Path:
    """Resolve canonical trace path. Never cwd-relative — must be single source."""
    env = os.environ.get("DECISION_RECALL_TRACE")
    if env:
        return Path(env).expanduser()
    return Path.home() / "decision-recall" / "state" / "recall_trace.jsonl"


def extract_text_from_transcript(transcript_path: str) -> str:
    """Read transcript JSONL, return text of the last assistant message.

    Transcript format: one JSON object per line. Each line typically has:
      {"type": "assistant", "message": {"role": "assistant", "content": [...]}}
    where content is a list of blocks (text, tool_use, etc.).

    We're tolerant: handle missing fields, string content, list content.
    Return "" on any failure.
    """
    try:
        p = Path(transcript_path)
        if not p.exists():
            return ""
        # Tail-read: scan backward for last assistant entry
        lines = p.read_text(errors="replace").splitlines()
    except Exception:
        return ""

    for raw in reversed(lines):
        if not raw.strip():
            continue
        try:
            entry = json.loads(raw)
        except Exception:
            continue
        # Different shapes seen in the wild — try a few keys
        msg = entry.get("message") or entry
        role = msg.get("role") or entry.get("type")
        if role != "assistant":
            continue
        content = msg.get("content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: list[str] = []
            for block in content:
                if isinstance(block, dict):
                    if block.get("type") == "text" and "text" in block:
                        parts.append(block["text"])
                    elif "text" in block:
                        parts.append(str(block["text"]))
            if parts:
                return "\n".join(parts)
        # Unknown shape — keep scanning earlier entries
    return ""


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

    # Avoid recursion if the hook itself triggers another Stop
    if data.get("stop_hook_active"):
        return 0

    # Primary path: transcript-based (current Claude Code spec)
    text = ""
    transcript_path = data.get("transcript_path")
    if transcript_path:
        text = extract_text_from_transcript(transcript_path)

    # Fallback: legacy inline field (older runtime / test harness)
    if not text:
        text = data.get("last_assistant_message", "")

    if not text or len(text) > 200000:
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
