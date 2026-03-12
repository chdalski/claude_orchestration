---
name: ensure-plans-dir
description: >
  Ensure the configured plans directory and its format
  guide exist before writing a plan. Run once before
  Phase 1 planning.
---

# /ensure-plans-dir

Prepare the plan directory before writing any plan files.
The Architect writes plans to the configured plans directory
and consults its `CLAUDE.md` for the required format —
without both, the planning flow breaks.

## Steps

1. **Find the plans directory** — read `.claude/settings.json`
   and extract `plansDirectory`. If the key is absent,
   default to `.ai/plans/`. This respects the project's
   configured location rather than assuming a fixed path.

2. **Check for the format guide** — use Read on
   `<plansDirectory>/CLAUDE.md`.

3. **If missing or outdated:**
   a. Read the canonical template from
      `.claude/templates/plan-format.md`.
   b. Write the template content to
      `<plansDirectory>/CLAUDE.md` using Write — this
      creates the directory if needed. Do not modify the
      template content. Keeping the format guide current
      ensures plans written across sessions follow the same
      structure.

4. **Read `<plansDirectory>/CLAUDE.md`** — load the format
   guide into context. Plans must follow this format so the
   lead and future sessions can parse them without guessing
   at conventions.
