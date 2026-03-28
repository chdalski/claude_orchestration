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

**All three steps below are mandatory — execute every step,
every time.** Do not skip step 2 or 3 because the directory
already exists or the format guide appears current. The
template may have changed since the last run, and skipping
the overwrite causes plans to follow a stale format. This
has caused real drift in production sessions.

## Steps

1. **Find the plans directory** — read `.claude/settings.json`
   and extract `plansDirectory`. If the key is absent,
   default to `.ai/plans/`. This respects the project's
   configured location rather than assuming a fixed path.

2. **Write the format guide (always — not conditional)** —
   if `<plansDirectory>/CLAUDE.md` already exists, Read it
   first — the Write tool requires a prior Read for existing
   files to prevent accidental overwrites. Then read the
   canonical template from
   `.claude/templates/plan-format.md` and write it to
   `<plansDirectory>/CLAUDE.md` using Write — this creates
   the directory if needed. Do not modify the template
   content. **Always overwrite, even if the file already
   exists** — the template may have changed since the last
   run, and only an unconditional write guarantees the
   deployed guide matches the current blueprint.

3. **Read `<plansDirectory>/CLAUDE.md`** — load the format
   guide into context. Plans must follow this format so the
   lead and future sessions can parse them without guessing
   at conventions.
