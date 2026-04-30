# Direct-Review

## When to Use

Use this workflow when the user prefers directness over
process and the plan meets both criteria:

1. **No security ramifications** — the change does not
   touch auth, input validation, cryptography, access
   control, or data handling that could introduce
   vulnerabilities
2. **Tests already cover it, or no tests are needed** —
   existing tests validate the behavior being changed,
   or the change is non-behavioral (typo, comment,
   documentation, config value)

Examples: fixing a typo, updating a config value,
renaming a variable, adjusting documentation.

Not appropriate when either criterion is not met — those
benefit from specialized agents (Test Engineer, Security
Engineer) that catch issues a single perspective would
miss.

## Agents

- **Reviewer** — independent quality gate, including
  CLAUDE.md drift detection. Created via `TeamCreate` as
  a one-agent team. The Reviewer composes the proposed
  commit message and returns it with the file list; the
  lead commits after user approval per CLAUDE.md's
  Committing Approved Work section.

## Flow

1. Lead implements the plan directly — read the relevant
   files first to ground the changes in current code.
2. Lead runs tests and linters if applicable — catching
   regressions before presenting to the Reviewer avoids
   wasted review cycles.
3. Lead creates a one-agent team via TeamCreate with the
   Reviewer.
4. Lead sends the work to the Reviewer with the plan's
   goal, context, and acceptance criteria so the Reviewer
   can verify scope completeness — Reviewer performs full
   review including CLAUDE.md drift detection. Even small
   changes can introduce drift (e.g., renaming a directory
   that CLAUDE.md references), and Direct-Review has the
   least process, making undetected drift most likely
   here. The handoff message must include an
   `advisor consultation status: none — Direct-Review
   workflow` line — the Reviewer rejects handoffs that
   omit this field.
5. If rejected: lead fixes issues and re-sends to Reviewer.
6. **User checkpoint** — lead presents the completed work,
   Reviewer's summary, and proposed commit message for
   user approval.
7. If approved, lead commits per CLAUDE.md's Committing
   Approved Work section.
8. If changes are needed, lead adjusts and returns to
   step 2.

## Completion Criteria

- Plan implemented as approved
- Tests pass (if applicable)
- Reviewer has approved the result (including drift check)
- User has approved the result
- Work committed by the lead
