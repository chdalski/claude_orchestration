---
name: ensure-ai-dirs
description: >
  Ensure the configured plans and memory directories exist,
  sync the plan format guide and review checklist, and
  move completed and canceled plans into the frozen
  completed/ directory. Run once before planning begins.
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
Do not skip step 4 because no plan appears finished — the
scan is cheap and the skill is idempotent when nothing
needs moving.

## Steps

1. **Read settings** — read `.claude/settings.json` and
   extract both `plansDirectory` and `autoMemoryDirectory`.

   If either key is **absent**: the blueprint expects both
   directories configured. Silently defaulting would leave
   the configuration missing for future sessions and other
   agents. Instead:

   a. Read `.claude/settings.local.json` if it exists
      (it may contain other local overrides that must be
      preserved).
   b. Add the missing key(s) to the parsed object (or
      create a new object if the file does not exist):
      - `"plansDirectory": ".ai/plans/"` if absent
      - `"autoMemoryDirectory": ".ai/memory/"` if absent
   c. Write the result back to `.claude/settings.local.json`.
   d. Report which keys were not configured and have been
      set in `settings.local.json` — the lead must relay
      this to the user so they can move the settings to
      `settings.json` if they want them version-controlled.

   Using `settings.local.json` (not `settings.json`)
   avoids modifying the checked-in blueprint configuration.
   Claude Code merges both files at startup, so the
   settings take effect immediately.

2. **Sync the plans directory files** — sync four files
   from `.claude/skills/ensure-ai-dirs/` into
   `<plansDirectory>`. Always read both source and target
   and compare them:

   a. **Plan format guide** — read the canonical template
      from `.claude/skills/ensure-ai-dirs/plan-format.md`.
      Read `<plansDirectory>/plan-format.md` if it exists.
      If the file does not exist or its content differs
      from the template, write the template to
      `<plansDirectory>/plan-format.md` using Write.

   b. **Plans CLAUDE.md** — read the template from
      `.claude/skills/ensure-ai-dirs/claude-md-template.md`.
      Read `<plansDirectory>/CLAUDE.md` if it exists. If
      the file does not exist or its content differs from
      the template, write the template to
      `<plansDirectory>/CLAUDE.md` using Write.

   c. **Plan review checklist** — read the template from
      `.claude/skills/ensure-ai-dirs/plan-review-checklist.md`.
      Read `<plansDirectory>/plan-review-checklist.md` if
      it exists. If the file does not exist or its content
      differs from the template, write the template to
      `<plansDirectory>/plan-review-checklist.md` using
      Write. The plan review subagent reads this checklist
      at review time — syncing it here ensures the
      checklist is current before any plan is written.

   d. **Completed plans CLAUDE.md** — create
      `<plansDirectory>/completed/` if it does not exist.
      Read the template from
      `.claude/skills/ensure-ai-dirs/completed-claude-md-template.md`.
      Read `<plansDirectory>/completed/CLAUDE.md` if it
      exists. If the file does not exist or its content
      differs from the template, write the template to
      `<plansDirectory>/completed/CLAUDE.md` using Write.
      Claude Code loads this file whenever an agent reads
      a plan in `completed/`, so every reader of a
      finished plan learns that it is frozen.

   e. Report whether updates were written or the files
      were already identical.

   This step is unconditional — execute it every time,
   even if the files appear current. The plans CLAUDE.md is
   intentionally slim — it points agents to plan-format.md
   rather than embedding the full format guide, so agents
   reading plans do not load the format guide into their
   context unnecessarily. Only the agent writing plans
   reads plan-format.md on demand.

3. **Ensure the memory directory exists** — create
   `<autoMemoryDirectory>` if it does not exist. No format
   guide is needed — Claude Code manages memory files
   directly. Report whether the directory was created or
   already existed.

4. **Move finished plans to `completed/`** — move every
   `Completed` or `Canceled` plan from `<plansDirectory>`
   into `<plansDirectory>/completed/`, the frozen plan
   log. The active directory then holds only plans that
   still need work.

   a. List files in `<plansDirectory>` matching the plan
      filename pattern `YYYY-MM-DD-*.md`. Exclude the
      synced files (`CLAUDE.md`, `plan-format.md`,
      `plan-review-checklist.md`) and the `completed/`
      subdirectory itself.

   b. For each plan file, read the `**Status:**` line
      from the header:
      - `Completed (YYYY-MM-DD)` or `Canceled` — move it,
        however recently it finished.
      - `NotStarted` or `InProgress` — leave it in place.

   c. Move each finished plan into
      `<plansDirectory>/completed/` using
      `git mv <src> <dst>` so git tracks the rename and
      history is preserved. If a plan is untracked,
      `git mv` refuses it — use plain `mv` for that plan.

   d. Report which plans were moved, or state that none
      were finished.
