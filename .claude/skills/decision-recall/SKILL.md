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

## Auto-suggest mode (proactive)

When the user reaches a clear judgment moment in conversation, **suggest** logging it — don't auto-save without permission.

Trigger to suggest:
- User explicitly states a choice ("Let's go with A", "We'll skip B", "Decided to ...")
- User identifies a non-obvious cause or pattern ("Turns out the issue is X, not Y")
- User sets a rule for future behavior ("From now on, we'll always ...")

When triggered, ask exactly:

> 📓 Want me to record this as a `<type>` marker?
>
> ```
> <type>: <topic-slug> | <one-line content>
> ```
>
> (`y` = save / `n` = skip / `e` = let me edit first)

Rules for the suggestion:
1. **Auto-generate the marker** from conversation context (topic + content) — don't ask the user to write it
2. **Max 1 suggestion per assistant turn** (no spam)
3. **Don't suggest** for: routine status, code edits, casual questions, things already visible in git/code
4. **Don't suggest** if 3 markers were already saved in the last 10 turns (avoid over-marking)
5. On `y`: run `decision-extractor` agent with the proposed marker
6. On `n`: skip silently, do not ask again about the same topic
7. On `e`: show the proposed marker, let user reword, then save

## Manual mode (always available)

User can also write markers directly:

```
결정 / decision: <topic> | <content>
판단 / analysis: <topic> | <content>
원칙 / principle: <topic> | <content>
```

When manual markers appear in conversation, run `decision-extractor` automatically (no suggestion needed — user already decided).

## How it works

Three marker types:
- `결정 / decision:` — a choice was made (what to do)
- `판단 / analysis:` — an observation or analysis (what was found)
- `원칙 / principle:` — a rule or pattern (what holds going forward)

Both Korean and English forms are valid. The extractor accepts both.

Each marker captured with `topic | one-line content` format, appended to `~/decision-recall/state/recall_trace.jsonl` (single canonical path — same across all projects; override with `$DECISION_RECALL_TRACE` env if needed).

## When to invoke which agent

- **decision-extractor**: Called when meaningful decisions/analyses/principles appear in the conversation. Scans the assistant's most recent response for the three marker types, normalizes, and appends to trace.
- **recall-viewer**: Called when user invokes `/recall` (timeline view) or asks "why did I decide X?". Loads `~/decision-recall/state/recall_trace.jsonl` (or `$DECISION_RECALL_TRACE` if set), filters by date/topic/keyword, and shows results.

## References

- `references/marker_format.md` — exact marker syntax + extraction rules
- `references/diary_guide.md` — when to mark vs not mark (avoid noise)

## Privacy invariant (★ critical)

- Trace lives in **`~/decision-recall/state/recall_trace.jsonl` (local only)** — never committed (`.gitignore`)
- This skill does **not transmit your trace to any server**
- Skill installer (the person who made this) **cannot access your trace**
- Your trace is yours; deletion = remove the file

## Boundary

This skill records and recalls. It does **not** judge your decisions, predict outcomes, or compare you to others. Use it as a memory aid, not as an oracle.
