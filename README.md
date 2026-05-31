# Decision Recall

> Record decisions as they happen. Recall them 3 months later.

A Claude Code skill that automatically captures the judgments you make in conversation (`결정:` / `판단:` / `원칙:`) and lets you ask `/recall` weeks or months later to see why you decided what you decided.

## What it solves

Three months from now, you'll forget *why* you chose X over Y. The decision still works (mostly), but the *reasoning* is gone. When the situation comes back, you re-litigate the whole thing.

This skill records the reasoning at the moment it happens, in a tiny, structured format. Later, you ask `/recall` and the past comes back.

## What it is not

- Not a meeting notes tool
- Not a journal
- Not a productivity tracker
- Not a coach
- It does not judge, predict, or compare

## Install

```bash
# 1. Clone into your project (or anywhere in your home dir)
git clone https://github.com/Nick-heo-eg/decision-recall.git ~/decision-recall

# 2. Symlink the skill into Claude Code's skill directory
mkdir -p ~/.claude/skills
ln -s ~/decision-recall/.claude/skills/decision-recall ~/.claude/skills/decision-recall

# 3. Symlink commands and agents (if you want global access)
mkdir -p ~/.claude/commands ~/.claude/agents
ln -s ~/decision-recall/.claude/commands/recall.md ~/.claude/commands/recall.md
ln -s ~/decision-recall/.claude/commands/recall-search.md ~/.claude/commands/recall-search.md
ln -s ~/decision-recall/.claude/agents/decision-extractor.md ~/.claude/agents/decision-extractor.md
ln -s ~/decision-recall/.claude/agents/recall-viewer.md ~/.claude/agents/recall-viewer.md

# 4. Restart Claude Code
```

Verify: type `/recall` in Claude Code. You should see "no trace yet, start using the skill".

## First 5 minutes

1. In any Claude Code conversation, when you reach a real decision, write it in this format:

   ```
   결정: q3-strategy | Pivot from feature expansion to retention
   판단: user-churn | 60% of churn happens in week 1
   원칙: code-review | PRs over 500 lines must be split
   ```

   (English aliases work too: `decision:`, `analysis:`, `principle:`)

2. Ask Claude to invoke `decision-extractor` on its last response (or it may do this automatically when the skill is loaded).

3. After a few decisions, run `/recall` to see them.

4. Later: `/recall q3-strategy` or `/recall 2026-05` to filter.

## Privacy

- Your trace lives in `state/recall_trace.jsonl` — local only
- `.gitignore` excludes it; it is never committed
- The skill does not transmit your trace anywhere
- The author of this skill **cannot access your trace**
- To delete: `rm state/recall_trace.jsonl`

## Boundary

This skill helps you remember what you decided. It will not tell you whether you were right, what to do next, or how you compare to others. That's your job.

## License

MIT
