---
name: example-mapping
description: >
  Interactive Example Mapping facilitator. Discovers
  rules, concrete examples, and open questions for a
  feature through Q&A with the user, then writes a
  structured mapping markdown file that can be passed to
  /test-list as the TDD entry path or used as informal
  context during clarification.
---

# /example-mapping

Conduct an interactive Example Mapping session for a
feature the user wants to implement. The output is a
markdown file with the story, rules, examples, and any
unresolved questions — the canonical input format that
`/test-list` consumes when the user wants to drive the
work via TDD, and a useful clarification artifact even
when the user does not.

## When to Invoke

Invoke when:

- The user wants to explore a feature before writing any
  test list or plan
- The feature has business rules and concrete behaviors
  worth surfacing through conversation rather than
  assumption

## Refusal Cases

Do **not** run when:

- The user has not described a feature to explore — ask
  for the feature description first; refuse to invent
  one
- The user wants you to "just write the rules yourself"
  — example mapping requires the user's domain
  knowledge; a fabricated mapping silently locks the
  implementor to behavior the user never authorized
- A current example mapping for this feature already
  exists and the user has not asked to refresh it —
  drift between versions silently diverges the
  implementor from the latest. Ask whether to amend the
  existing file rather than overwrite

## Core Discipline — Facilitate, Do Not Invent

You do **not** know the domain; the user does. Your job
is to **ask**, not to assume.

- **NEVER invent a rule.** Ask the user what the rules
  are.
- **NEVER invent an example.** Ask the user for concrete
  inputs and expected outputs.
- **NEVER assume boundary behavior** (empty input, max
  values, error cases). Ask.
- **NEVER fill in gaps yourself.** When something is
  unclear, create an open question (red card) and ask.
- **NEVER continue past an unclear point.** Stop, ask,
  and resolve before moving on.

A facilitator that fills in answers produces a mapping
that looks complete but encodes the *facilitator's*
guesses, not the user's domain knowledge. The
implementor then builds the wrong feature against a
mapping that cannot be challenged because nobody
remembers which entries were guessed and which came
from the user.

## Steps

**All steps are mandatory.** Do not skip step 5
(user review) on the grounds that the draft looks
internally consistent — the user is the only authority
on whether the mapping captures their intent.

1. **Identify the story.** Ask: "What feature are we
   exploring?" Capture as a one-sentence story (the
   yellow card). If the user supplies a card image or
   prior description, use it as the starting point and
   confirm before proceeding.

2. **Discover rules.** Ask the user — never list them
   yourself — what the rules are. Probe with targeted
   questions:
   - "What happens with empty / zero input?"
   - "Are there limits, caps, or thresholds?"
   - "Are there special cases or exceptions?"
   - "Does this feature interact with anything else?"

   Use `AskUserQuestion` for structured options when
   you need to disambiguate between specific
   possibilities. Each distinct rule becomes a blue
   card. Confirm each rule with the user before
   recording it.

3. **Find examples per rule.** For each rule, ask the
   user for concrete examples — specific inputs and
   expected outputs. If the user gives vague answers
   ("a few items get a discount"), drill in until the
   numbers are concrete ("how many items? what
   discount?"). Each example becomes a green card.
   Include both straightforward cases and boundary
   cases (the smallest, the largest, the just-over-the-
   threshold).

4. **Track and resolve open questions.** When something
   is unclear, immediately create a red card. Resolve
   in real time via `AskUserQuestion` when the user can
   answer; leave as a red card when the user cannot. Do
   **not** guess answers to convert red cards into
   blue/green ones — an unresolved question is more
   honest than a fabricated rule.

5. **Review with the user.** Before writing the file,
   present a summary of all discovered rules, examples,
   and open questions. Ask: "Is this complete? Did I
   miss anything?" Iterate on additions until the user
   confirms.

6. **Write the mapping file.** Ask the user where to
   save the file. Default to
   `<feature-slug>-example-mapping.md` in the project
   root if the user does not specify. Use this
   structure:

   ```markdown
   # Example Mapping: <feature name>

   ## Story

   <one-sentence user story>

   ## Rules

   ### Rule 1: <rule name>

   <description>

   ### Rule 2: <rule name>

   <description>

   ## Examples

   ### For Rule 1: <rule name>

   - <input> → <expected output>
   - <input> → <expected output>

   ### For Rule 2: <rule name>

   - <input> → <expected output>

   ## Open Questions

   - <question 1>
   - <question 2>
   ```

   Omit the Open Questions section entirely if no red
   cards remain.

7. **Report and suggest the next step.** Tell the user:
   - The file path that was written
   - The health indicators (see below)
   - The recommended next action

## Health Indicators

Report after writing the file:

| Indicator | Status | Meaning |
|---|---|---|
| Many open questions (>3) | Not ready | Feature needs more discussion before tests can be derived |
| Many rules (>6) | Too large | Consider splitting into multiple features, each with its own mapping |
| Few examples per rule (<2) | Thin coverage | More concrete examples would strengthen the eventual test list |
| Balanced (rules covered by examples, few or no questions) | Ready | Proceed to /test-list or use as clarification context |

## Next Step

After writing the file, suggest exactly one of:

- **If healthy and the user is doing TDD:** "Invoke
  `/test-list <path-to-mapping>` to convert the
  examples into a TDD test list."
- **If healthy and TDD is not the chosen path:** "The
  mapping is ready as clarification context — describe
  what you want to build and the lead will incorporate
  the rules and examples into the plan."
- **If too many open questions remain:** "Resolve the
  open questions (offline or with stakeholders), then
  amend the file or re-invoke the skill."
- **If too large:** "Split the feature into smaller
  stories — each with its own mapping — before
  proceeding."

The skill does not commit the user to TDD. The mapping
file is reusable as project documentation, as input to
`/test-list`, or as informal context during the lead's
clarification flow — workflow-neutral by design.

## Anti-Patterns

- **Inventing rules.** "I assume the score caps at 6." →
  Wrong. Ask: "Is there a cap?"
- **Guessing examples.** "For 3 cards you probably get 9
  points." → Wrong. Ask: "How many points for 3 cards?"
- **Skipping questions.** Sensing ambiguity but not
  asking. → Wrong. Always create a red card and ask.
- **Writing without confirmation.** Producing the file
  before the user reviews the summary. → Wrong. Always
  confirm first.
- **Silent overwrite.** Re-running on a mapping the user
  has not asked you to refresh. → Wrong. Ask whether
  to amend the existing file rather than overwrite.
