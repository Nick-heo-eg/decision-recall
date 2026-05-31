# Marker Format

Three marker types, one line each.

## Syntax

```
<type>: <topic> | <one-line content>
```

- **`<type>`** — one of: `결정` / `판단` / `원칙` / `decision` / `analysis` / `principle`
- **`<topic>`** — short slug (1-3 words, no spaces preferred, e.g. `samsung-merger`, `q3-strategy`)
- **`<content>`** — one line, the actual judgment (≥ 10 characters)

## Examples

### 결정 (decision) — a choice that was made

```
결정: q3-strategy | Pivot from feature expansion to retention metrics
decision: hiring-freeze | Pause backend hiring through end of Q3
```

### 판단 (analysis) — an observation, what was found

```
판단: user-churn | 60% of churn happens in first 7 days; onboarding is the lever
analysis: api-latency | p99 spiked after deploy 142; rollback fixed it
```

### 원칙 (principle) — a rule or pattern

```
원칙: code-review | Every PR over 500 lines must be split; no exceptions
principle: meeting-notes | Action items must have an owner and a date
```

## What counts as "meaningful"

Mark when:
- A choice was made between alternatives
- A non-obvious pattern was identified
- A rule was set for future behavior
- You want to find this 3 months later

Don't mark:
- Routine status updates ("commit done", "test passed")
- Pure information ("the API returns JSON")
- Speculation without a decision ("we could try X")

## Anti-patterns

- ❌ More than 5 markers in one response (signal of over-marking)
- ❌ `결정: stuff | did things` (vague topic and content)
- ❌ Marking everything (defeats the purpose — recall becomes noisy)
- ❌ Duplicating a recent marker (extractor dedups automatically, but write tighter content)
