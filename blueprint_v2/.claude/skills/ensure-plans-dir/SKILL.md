---
name: ensure-plans-dir
description: >
  Ensure .ai/plans/ and its format guide exist before
  writing a plan. Run once at the start of Phase 1 planning.
---

# /ensure-plans-dir

Prepare the plan directory before writing any plan files.
The Architect writes plans to `.ai/plans/` and consults
`.ai/plans/CLAUDE.md` for the required format — without
both, the planning flow breaks. Running this at the start
of Phase 1 means only the agent that actually needs the
directory is responsible for creating it.

## Steps

1. **Check for the format guide** — use Read on
   `.ai/plans/CLAUDE.md`.

2. **If missing or outdated:**
   a. Read the canonical template from
      `.claude/templates/plan-format.md`.
   b. If `.ai/plans/CLAUDE.md` is missing or its content
      differs from the template, write the template content
      to `.ai/plans/CLAUDE.md` using Write — this creates
      the directory if needed. Do not modify the template
      content. Keeping the format guide current ensures
      plans written across sessions follow the same
      structure.

3. **Read `.ai/plans/CLAUDE.md`** — load the format guide
   into context. Plans must follow this format so the lead
   and future sessions can parse them without guessing at
   conventions.
