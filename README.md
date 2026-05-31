# Decision Recall

A Claude Code skill for remembering *why* you decided what you decided.

---

## The problem

You make hundreds of small judgment calls — at work, in code, in life. Three months later, the decision still stands, but the reasoning behind it is gone. So when a similar situation comes around, you re-litigate the whole thing from scratch.

Examples:

- **At work**: "Why did we pick vendor A over B?" — the contract is signed, but nobody remembers the trade-offs.
- **In code**: "We agreed not to use this pattern... why was that again?"
- **In life**: A friend brings up the exact dilemma you wrestled with last year. You solve it from zero, again.
- **In meetings**: The same debate, six months apart, with the same conclusion. Hours lost.

The outcome survives. The reasoning evaporates.

## What this skill does

While you're working in Claude Code, when you reach a real decision, you write one line:

```
decision: vendor-choice | Picked A over B — A's SLA is 99.9% vs B's 99.5%, matters for our compliance
```

Three months later, when the question comes back:

```
/recall vendor
```

You get the line back. The reasoning is there, not just the conclusion.

## What this skill is not

- **Not a meeting notes tool.** You don't log everything — only what's worth remembering.
- **Not a journal.** No feelings, no daily logs.
- **Not a productivity tracker.** No counts, no streaks, no scoring.
- **Not a coach.** It won't tell you whether you were right.

It's a memory aid. You judge. The tool returns the judgment when you ask.

## How it works

Two ways to capture:

**1. Auto-suggest (default)** — Claude watches the conversation. When a clear decision happens, it asks:

> 📓 Want me to record this as a `decision` marker?
> `decision: vendor-choice | Picked A over B — SLA matters for compliance`
> (`y` = save / `n` = skip / `e` = edit)

You just answer `y/n/e`. No formatting required.

**2. Manual** — write the marker yourself if you prefer:

| Marker | When to use | Example |
|---|---|---|
| `결정 / decision` | You picked between options | `decision: hiring \| Pause backend hiring through Q3, focus on infra` |
| `판단 / analysis` | You found a non-obvious cause or pattern | `analysis: churn \| 60% of churn happens in week 1 — onboarding is the lever` |
| `원칙 / principle` | You set a rule going forward | `principle: pr-size \| Every PR over 500 lines must be split` |

Both Korean and English forms work. The extractor accepts both.

When markers appear in a conversation, the `decision-extractor` agent appends them to a local file (`state/recall_trace.jsonl`). The `/recall` command reads that file back.

## Install (5 minutes)

```bash
# 1. Clone
git clone https://github.com/Nick-heo-eg/decision-recall.git ~/decision-recall

# 2. Link into Claude Code
mkdir -p ~/.claude/skills ~/.claude/commands ~/.claude/agents
ln -s ~/decision-recall/.claude/skills/decision-recall ~/.claude/skills/decision-recall
ln -s ~/decision-recall/.claude/commands/recall.md ~/.claude/commands/recall.md
ln -s ~/decision-recall/.claude/commands/recall-search.md ~/.claude/commands/recall-search.md
ln -s ~/decision-recall/.claude/agents/decision-extractor.md ~/.claude/agents/decision-extractor.md
ln -s ~/decision-recall/.claude/agents/recall-viewer.md ~/.claude/agents/recall-viewer.md

# 3. Restart Claude Code
```

Verify: type `/recall` in Claude Code. You should see `no trace yet, start using the skill`.

Full guide: [docs/install_guide.md](docs/install_guide.md)

## First 5 minutes

→ [docs/quickstart.md](docs/quickstart.md) — walk through one realistic decision end to end.

## Privacy

- Your trace lives in **one local file**: `state/recall_trace.jsonl`
- `.gitignore` excludes it. It is never committed.
- The skill makes no network calls beyond what Claude Code itself does.
- The author of this skill **cannot access your trace**.
- To delete everything: `rm state/recall_trace.jsonl`

Details: [docs/privacy.md](docs/privacy.md)

## License

MIT
