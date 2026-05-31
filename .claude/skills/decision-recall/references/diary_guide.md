# Diary Guide — when to mark, when not to

The skill's value comes from **signal, not volume**. A trace with 50 high-signal entries beats a trace with 500 noise entries.

## Rule of thumb

> **"Would I want to remember this in 3 months?"**

- **Yes** → mark it
- **No** → don't mark it

## When to mark (do this)

- A decision between options was made ("we chose A over B")
- A non-obvious cause was found ("the slowdown is the cache, not the DB")
- A rule was set ("from now on, all migrations must be reviewed")
- A constraint was discovered ("we can't go above 100 concurrent users without sharding")
- A surprising pattern was noticed ("users who use feature X retain 3x longer")

## When not to mark (skip these)

- Routine confirmations ("file saved", "test passed")
- Pure restating of facts ("the function returns null")
- Speculation that didn't become a decision ("maybe we could try X")
- Things you'll see in the code anyway ("renamed the variable")
- Conversational filler ("OK, sounds good")

## The 3-month test

Imagine you come back to this conversation in 3 months. Which entries would you actually *want* to surface?

Mark **those**. Skip the rest.

## When the extractor over-marks

If `decision-extractor` finds 5+ markers in one response, it warns and stops. This is intentional — over-marking dilutes recall quality. If you genuinely have 5+ distinct decisions, you're probably bundling too many things in one response; consider splitting.

## What this skill is not

- **Not a meeting notes tool** — it's a decision lineage tool
- **Not a journal** — it's selective
- **Not a productivity tracker** — no counts, no streaks
- **Not a coach** — no advice, just memory
