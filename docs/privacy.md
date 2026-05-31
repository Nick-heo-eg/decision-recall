# Privacy

## Your data stays on your machine

- The trace is stored in `state/recall_trace.jsonl`, in this repo
- `.gitignore` excludes it from commits
- The skill never transmits the trace to any server
- The author of this skill **cannot access your trace**, period

## What the skill reads/writes

| File | Direction | Purpose |
|---|---|---|
| `state/recall_trace.jsonl` | read + append | your decision history |
| `~/.claude/skills/decision-recall/SKILL.md` | read | skill orchestrator |
| `~/.claude/agents/*.md` | read | agent definitions |

The skill does not read other files on your machine. The skill does not make network calls.

## What gets logged (model-side)

When Claude runs an agent, the agent's reasoning happens through Claude's API. This means:
- The text Claude sees during extraction (your last message) goes through Anthropic's API
- Anthropic's own data handling policies apply: https://www.anthropic.com/legal/commercial-terms
- This skill itself stores nothing remotely

## Deletion

```bash
rm state/recall_trace.jsonl
```

That's it. There is no backup, no sync, no copy.

## What this skill is not

- Not a SaaS product
- Not a server
- Not an account-based system
- Not telemetry-instrumented

It's a local file plus some markdown that tells Claude how to read and write it.

## If you share this skill

If you fork or clone and share with others, make sure they understand:
- Their trace is **their** local file
- Your install of the skill cannot see their trace
- Their install of the skill cannot see your trace
