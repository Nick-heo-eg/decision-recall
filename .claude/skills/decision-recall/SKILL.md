---
name: decision-recall
description: Record decisions as they happen, recall them 3 months later. Auto-captures judgment markers from your Claude Code conversations and lets you ask "why did I decide X?" weeks or months later.
---

# Decision Recall

A Claude Code skill for **decision lineage preservation**.

## What it does

Captures decisions, analyses, and principles from your Claude Code conversations into a local trace file. Later, ask `/recall` to see why you made a decision weeks or months ago.

**Use this skill when**:
- User invokes `/recall` or `/recall-search`
- User asks "why did I decide X?" or "what did I conclude about Y?"
- User says "remember when we decided..."
- A meaningful judgment is being made and should be logged

## How it works

Three marker types automatically extracted from conversations:
- `결정:` / `decision:` — a choice was made (what to do)
- `판단:` / `analysis:` — an observation or analysis (what was found)
- `원칙:` / `principle:` — a rule or pattern (what holds going forward)

Each marker captured with `topic | one-line content` format, appended to `state/recall_trace.jsonl`.

## When to invoke which agent

- **decision-extractor**: Called when meaningful decisions/analyses/principles appear in the conversation. Scans the assistant's most recent response for the three marker types, normalizes, and appends to trace.
- **recall-viewer**: Called when user invokes `/recall` (timeline view) or asks "why did I decide X?". Loads `state/recall_trace.jsonl`, filters by date/topic/keyword, and shows results.

## References

- `references/marker_format.md` — exact marker syntax + extraction rules
- `references/diary_guide.md` — when to mark vs not mark (avoid noise)

## Privacy invariant (★ critical)

- Trace lives in **`state/recall_trace.jsonl` (local only)** — never committed (`.gitignore`)
- This skill does **not transmit your trace to any server**
- Skill installer (the person who made this) **cannot access your trace**
- Your trace is yours; deletion = remove the file

## Boundary

This skill records and recalls. It does **not** judge your decisions, predict outcomes, or compare you to others. Use it as a memory aid, not as an oracle.
