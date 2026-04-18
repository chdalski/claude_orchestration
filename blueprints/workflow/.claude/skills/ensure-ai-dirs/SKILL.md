---
name: ensure-ai-dirs
description: >
  Ensure the configured plans and memory directories exist,
  sync the plan format guide and review checklist, and
  archive completed plans older than 14 days. Run once
  before Phase 1 planning.
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
Do not skip step 4 because no plans appear old enough to
archive — the scan is cheap and the skill is idempotent
when nothing is archivable.

## Steps

1. **Read settings** — read `.claude/settings.json` and
   extract both `plansDirectory` and `autoMemoryDirectory`.
   If either key is absent, default to `.ai/plans/` and
   `.ai/memory/` respectively. This respects the project's
   configured locations rather than assuming fixed paths.

2. **Sync the plans directory files** — sync three files
   from `.claude/skills/ensure-ai-dirs/` to `<plansDirectory>`:

   a. **Plan format guide** — read the canonical template
      from `.claude/skills/ensure-ai-dirs/plan-format.md`. Read
      `<plansDirectory>/plan-format.md` if it exists. If
      the file does not exist or its content differs from
      the template, write the template to
      `<plansDirectory>/plan-format.md` using Write.

   b. **Plans CLAUDE.md** — read the template from
      `.claude/skills/ensure-ai-dirs/claude-md-template.md`. Read
      `<plansDirectory>/CLAUDE.md` if it exists. If the
      file does not exist or its content differs from the
      template, write the template to
      `<plansDirectory>/CLAUDE.md` using Write.

   c. **Plan review checklist** — read the canonical
      template from
      `.claude/skills/ensure-ai-dirs/plan-review-checklist.md`.
      Read `<plansDirectory>/plan-review-checklist.md` if it
      exists. If the file does not exist or its content
      differs from the template, write the template to
      `<plansDirectory>/plan-review-checklist.md` using
      Write.

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

4. **Archive old plans** — scan `<plansDirectory>` for
   completed or canceled plans older than 14 days and
   move them to `<plansDirectory>/archive/`. Archiving
   keeps the active plans directory focused on in-progress
   work while preserving history.

   a. List files in `<plansDirectory>` matching the plan
      filename pattern `YYYY-MM-DD-*.md`. Exclude the
      synced files (`CLAUDE.md`, `plan-format.md`,
      `plan-review-checklist.md`) and the `archive/`
      subdirectory itself.

   b. For each plan file, read the `**Status:**` line
      from the header:
      - `Canceled` — always archive (no useful date; the
        plan is terminated).
      - `Completed (YYYY-MM-DD)` — archive if the recorded
        date is more than 14 days before today.
      - `NotStarted` or `InProgress` — never archive.

   c. If there are any plans to archive:
      - Create `<plansDirectory>/archive/` if it does not
        exist.
      - Move each archivable plan using
        `git mv <src> <dst>` so git tracks the rename and
        history is preserved.

   d. Report which plans were archived, or state that none
      were archivable.

   The 14-day window preserves recent completions in the
   active directory — a user asking "what did we just
   finish" sees recent work without digging into the
   archive. Canceled plans bypass the window because they
   are terminated, not completed, and have no remaining
   value in the active view.
