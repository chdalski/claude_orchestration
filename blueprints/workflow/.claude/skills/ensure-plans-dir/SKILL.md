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

**Both steps below are mandatory — execute every step,
every time.** Do not skip step 2 because the directory
already exists or the format guide appears current.

## Steps

1. **Find the plans directory** — read `.claude/settings.json`
   and extract `plansDirectory`. If the key is absent,
   default to `.ai/plans/`. This respects the project's
   configured location rather than assuming a fixed path.

2. **Sync the format guide** — read the canonical template
   from `.claude/templates/plan-format.md`. Then read
   `<plansDirectory>/CLAUDE.md` if it exists. If the file
   does not exist or its content differs from the template,
   write the template to `<plansDirectory>/CLAUDE.md` using
   Write. If the content is identical, no write is needed.
   The template and the format guide are now both in
   context — plans must follow this format so future
   sessions can parse them without guessing at conventions.
