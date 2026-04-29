---
name: test-list
description: >
  TDD entry path. Convert a user-supplied example mapping
  into a minimum-required test list via the test-list
  subagent. Hands back a user-confirmed list; the lead
  then writes the plan with the test list embedded and
  proceeds with TDD-filtered workflow selection per the
  "When the User Invokes /test-list" section in the
  lead's CLAUDE.md.
---

# /test-list

The `/test-list` skill is the TDD entry path. The user
invokes it with an example mapping; the skill produces a
user-confirmed minimum required test list and commits the
task to the TDD track. The skill's scope stops at
"user-confirmed test list" — plan writing, plan-reviewer
cycle, plan approval, workflow selection, team setup, and
execution are the lead's normal flow described in **When
the User Invokes /test-list** in the lead's CLAUDE.md.
Keeping the skill workflow-neutral means it stays usable
across any workflow the `tdd-*` filter surfaces.

## When to Invoke

Invoke when all hold:

- The user wants to develop a feature using TDD
- An example mapping for the feature exists (image or
  markdown)
- The target language and test framework are known
  (either from project context or from clarification)
- No in-progress plan for this task exists yet

## Refusal Cases

Do **not** run this skill when any of these hold — stop,
explain why, and point the user to the correct path:

- **Non-code task** (documentation, prose edits,
  config-only changes). TDD does not apply; use the
  normal clarification flow.
- **In-progress plan exists for this task.** Resume the
  existing plan instead (see *Resuming Work* in the
  lead's CLAUDE.md) — running the skill would fork the
  work.
- **No example mapping and the user declines to create
  one.** The skill depends on grounded rules and
  examples; a fabricated list would silently commit the
  implementor to the wrong behavior. Fall back to the
  normal clarification flow.
- **Target language/test framework not known.** The test
  list uses the target framework's pending-test idiom
  (e.g. Vitest `it.todo(...)`, pytest
  `@pytest.mark.skip`). Clarify the target with the user
  first, then invoke the skill — do not guess.

## Steps

**All steps are mandatory.** Do not skip step 4 on the
grounds that the draft looks internally consistent —
ordered simple → complex, descriptions clear, every rule
covered, no implementation hints. None of those signals
justify skipping confirmation. The user may spot missing
behaviors that require domain knowledge the subagent did
not have, prefer different prioritization, or want
entries the draft gives no reason to include. Only the
user's confirmation converts the draft into a binding
acceptance criterion.

1. **Collect the example mapping.** The user supplies it
   with the invocation — typically an image pasted into
   the CLI, or a path to a markdown file. Inspect pasted
   images directly; open markdown paths with Read. If
   nothing was supplied, ask the user before proceeding.

2. **Launch the test-list subagent.** Use the `Agent`
   tool with `subagent_type: "test-list"`. In the prompt,
   include the example mapping content (transcribe from a
   pasted image; pass the path if markdown), **the target
   language and test framework** (required), and the
   remaining meta if known — feature name, target test
   file path, target implementation file path. Transcribe
   rather than attach: the subagent has `Read` only and
   cannot open in-chat attachments.

3. **Collect the subagent's output** per the agent's
   Output Format section — a framework-specific test case
   list (describe/test block with pending placeholders,
   no imports) followed by a metadata block (feature,
   target, advanced features, open questions). Both go
   into the plan verbatim under the **Minimum Required
   Tests** heading.

4. **Present to the user for confirmation.** Use
   `AskUserQuestion` to ask whether to proceed, add,
   remove, or revise entries. If the subagent surfaced
   unresolved red-card questions, raise them in the same
   turn — the user can answer or mark them as explicit
   uncertainties for the plan.

5. **Hand off.** Continue with the post-skill flow in
   the lead's CLAUDE.md under **When the User Invokes
   /test-list** — fill remaining clarification gaps,
   write the plan with the confirmed test list embedded
   under a **Minimum Required Tests** heading, run the
   plan-reviewer cycle and present the plan to the user
   for approval, then filter workflow options to TDD only
   when proposing the approach.
