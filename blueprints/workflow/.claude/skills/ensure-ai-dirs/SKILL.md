---
name: ensure-ai-dirs
description: >
  Ensure the configured plans and memory directories exist,
  and sync the plan format guide. Run once before Phase 1
  planning.
---

# /ensure-ai-dirs

Prepare the `.ai/` directories before writing any plan
files or storing memories. The Architect writes plans to
the configured plans directory and consults its `CLAUDE.md`
for the required format — without both, the planning flow
breaks. The memory directory must exist for Claude Code's
auto-memory system to persist memories across sessions.

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

2. **Sync the plan format guide** — read the canonical
   template from `.claude/templates/plan-format.md`. Then
   read `<plansDirectory>/CLAUDE.md` if it exists. If the
   file does not exist or its content differs from the
   template, write the template to
   `<plansDirectory>/CLAUDE.md` using Write. If the content
   is identical, no write is needed. The template and the
   format guide are now both in context — plans must follow
   this format so future sessions can parse them without
   guessing at conventions.

3. **Ensure the memory directory exists** — create
   `<autoMemoryDirectory>` if it does not exist. No format
   guide is needed — Claude Code manages memory files
   directly. Report whether the directory was created or
   already existed.
