---
name: ensure-ai-dirs
description: >
  Ensure the configured plans and memory directories exist,
  and sync the plan format guide. Run once before Phase 1
  planning.
---

# /ensure-ai-dirs

Prepare the `.ai/` directories before writing any plan
files or storing memories. The lead writes plans to the
configured plans directory and consults its `CLAUDE.md`
for the required format — without the directory, the
CLAUDE.md pointer, and the format guide, the planning
flow breaks. The memory directory must exist for Claude
Code's auto-memory system to persist memories across
sessions.

**All steps below are mandatory — execute every step,
every time.** Do not skip step 2 because the directory
already exists or the format guide appears current. Do not
skip step 3 because the memory directory already exists.

## Steps

1. **Read settings** — read `.claude/settings.json` and
   extract both `plansDirectory` and `autoMemoryDirectory`.
   If either key is absent, default to `.ai/plans/` and
   `.ai/memory/` respectively. This respects the project's
   configured locations rather than assuming fixed paths.

2. **Sync the plans directory files** — sync two files
   from `.claude/templates/` to `<plansDirectory>`:

   a. **Plan format guide** — read the canonical template
      from `.claude/templates/plan-format.md`. Read
      `<plansDirectory>/plan-format.md` if it exists. If
      the file does not exist or its content differs from
      the template, write the template to
      `<plansDirectory>/plan-format.md` using Write.

   b. **Plans CLAUDE.md** — read the template from
      `.claude/templates/claude-md-template.md`. Read
      `<plansDirectory>/CLAUDE.md` if it exists. If the
      file does not exist or its content differs from the
      template, write the template to
      `<plansDirectory>/CLAUDE.md` using Write.

   The CLAUDE.md is intentionally slim — it points agents
   to plan-format.md rather than embedding the full format
   guide, so agents reading plans do not load the format
   guide into their context unnecessarily. Only the agent
   writing plans reads plan-format.md on demand.

3. **Ensure the memory directory exists** — create
   `<autoMemoryDirectory>` if it does not exist. No format
   guide is needed — Claude Code manages memory files
   directly. Report whether the directory was created or
   already existed.
