# Install Guide — 5 minutes

## Prereqs

- Claude Code installed (`claude` CLI works)
- Git
- Mac/Linux (Windows: WSL recommended)

## Step 1: Clone

```bash
git clone https://github.com/Nick-heo-eg/decision-recall.git ~/decision-recall
```

## Step 2: Link the skill

```bash
mkdir -p ~/.claude/skills
ln -s ~/decision-recall/.claude/skills/decision-recall ~/.claude/skills/decision-recall
```

If you prefer copy over symlink (e.g. on Windows):
```bash
cp -r ~/decision-recall/.claude/skills/decision-recall ~/.claude/skills/
```

## Step 3: Link commands and agents (optional but recommended)

```bash
mkdir -p ~/.claude/commands ~/.claude/agents

ln -s ~/decision-recall/.claude/commands/recall.md ~/.claude/commands/recall.md
ln -s ~/decision-recall/.claude/commands/recall-search.md ~/.claude/commands/recall-search.md
ln -s ~/decision-recall/.claude/agents/decision-extractor.md ~/.claude/agents/decision-extractor.md
ln -s ~/decision-recall/.claude/agents/recall-viewer.md ~/.claude/agents/recall-viewer.md
```

## Step 4: Restart Claude Code

Close and reopen Claude Code so it picks up the new skill, agents, and commands.

## Step 5: Verify

In Claude Code, type:

```
/recall
```

Expected output:

```
No trace yet, start using the skill.
```

(If you get "unknown command", check that Step 3 succeeded.)

## First real use

In a normal Claude Code conversation, after you make a real decision, write one line in this format:

```
결정 / decision: <topic-slug> | <one-line content>
```

(Use whichever you prefer — both Korean `결정 / 판단 / 원칙` and English `decision / analysis / principle` are accepted.)

Then ask Claude:

> "Run the decision-extractor on your last message."

Claude will scan and add the marker to `~/decision-recall/state/recall_trace.jsonl`.

Now check:

```
/recall
```

You should see your entry.

## Troubleshooting

**"unknown command /recall"**
→ Step 3 was skipped or symlinks didn't resolve. Re-run Step 3.

**"no trace yet" but you wrote markers**
→ The `decision-extractor` agent didn't run yet. Ask Claude to invoke it on the previous message explicitly.

**"trace file not found"**
→ Make sure you're in the right cwd; `state/recall_trace.jsonl` is project-local. Or check `~/decision-recall/state/recall_trace.jsonl`.

**Markers extracted but content is empty**
→ Content must be ≥ 10 characters. Tighten your `| ...` portion.

## Step 6 (optional): install the auto-capture hook

By default, Claude will *ask* before saving a marker (`y/n/e`). If you want it to save **automatically** with no prompts:

```bash
~/decision-recall/hooks/install_hook.sh
```

What it does:
- Adds one entry to `~/.claude/settings.json` under `hooks.Stop`
- After every Claude response, the hook scans for markers (`결정/판단/원칙` or `decision/analysis/principle`) and appends matches to `~/decision-recall/state/recall_trace.jsonl`
- Idempotent — re-running won't duplicate the entry
- Self-contained: no network calls, no external dependencies, never blocks Claude

Restart Claude Code after install.

To uninstall the hook only: open `~/.claude/settings.json` and remove the entry under `hooks.Stop` whose `command` references `~/decision-recall/hooks/auto_capture.py`.

## Uninstall

```bash
rm ~/.claude/skills/decision-recall
rm ~/.claude/commands/recall.md ~/.claude/commands/recall-search.md
rm ~/.claude/agents/decision-extractor.md ~/.claude/agents/recall-viewer.md
# If you installed the auto-capture hook, edit ~/.claude/settings.json
# and remove the entry under hooks.Stop that references auto_capture.py
rm -rf ~/decision-recall
```

Your trace (`state/recall_trace.jsonl`) is deleted with the directory.
