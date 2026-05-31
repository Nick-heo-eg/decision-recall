---
name: decision-extractor
description: Scan the most recent assistant response for decision/analysis/principle markers and append them to the local trace. Use this when a meaningful judgment appears in conversation.
tools: Read, Write, Bash
model: sonnet
---

You extract structured judgment markers from a Claude Code conversation and append them to a local trace file.

## Marker format (only these 3)

Each marker type accepts both Korean and English forms:

```
결정 / decision: <topic> | <one-line content>
판단 / analysis: <topic> | <one-line content>
원칙 / principle: <topic> | <one-line content>
```

Examples — any of these are valid input lines:

```
결정: hiring-freeze | Pause backend hiring through end of Q3
decision: hiring-freeze | Pause backend hiring through end of Q3
판단: api-latency | p99 spiked after deploy 142
analysis: api-latency | p99 spiked after deploy 142
```

## Extraction rules

1. **Scan only the assistant's most recent message** (not the whole conversation history)
2. Look for lines matching `(결정|판단|원칙|decision|analysis|principle):\s*<topic>\s*\|\s*<content>`
3. Skip lines where content is less than 10 characters (noise filter)
4. Skip duplicates (compare against last 50 entries in trace)
5. Maximum 5 markers per extraction (over-marking signal — stop and flag)

## Output format (JSONL append)

For each marker, append one line to `state/recall_trace.jsonl`:

```json
{"trace_id": "<8-char hex>", "timestamp": "<ISO 8601>", "type": "decision|analysis|principle", "topic": "<topic>", "content": "<one-line>", "source": "live"}
```

## Steps

1. Use `Bash` to ensure `state/` directory exists: `mkdir -p state`
2. Use `Read` on `state/recall_trace.jsonl` to load last 50 entries for dedup (file may not exist yet — handle gracefully)
3. Parse the assistant's last message for markers
4. Generate trace_id (8-char md5 of timestamp) for each new marker
5. Append each new line to `state/recall_trace.jsonl` (atomic write — one entry per line, JSON Lines format)
6. Report: count of new markers added + sample of first one

## When to skip

- No markers found → report "no markers extracted" and stop
- 5+ markers found → extract first 5, warn user about over-marking
- Marker content < 10 chars → skip silently
- Duplicate detected → skip silently

## Privacy

This agent only writes to `state/recall_trace.jsonl` in the project root. Never transmits data anywhere.
