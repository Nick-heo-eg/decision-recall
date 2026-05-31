---
description: Show recent decisions, or filter by date/topic/keyword
argument-hint: [optional query: date, topic, or keyword]
---

Invoke the **recall-viewer** agent to display past judgments from `~/decision-recall/state/recall_trace.jsonl` (or `$DECISION_RECALL_TRACE` if set).

Query: $ARGUMENTS

If no query given, show the last 10 entries.

Otherwise, smart-search by:
- Date prefix (`2026-05` or `2026-05-30`)
- Topic name
- Keyword (case-insensitive substring in topic or content)
