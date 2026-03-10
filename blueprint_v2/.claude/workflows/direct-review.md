# Direct-Review

## When to Use

Use this workflow for tasks where the user
prefers directness over process, and the change is
well-understood. Examples: fixing a typo, updating a config
value, adding a simple function, renaming a variable,
adjusting documentation.

Not appropriate for cross-cutting design decisions,
security-sensitive changes, or when independent review is
needed — those benefit from specialized agents that catch
issues a single perspective would miss.

## Agents

- **Reviewer** — independent quality gate, including
  CLAUDE.md drift detection. Spawned via TeamCreate (a
  one-agent team) so it can receive the commit signal
  after the user checkpoint. The Reviewer composes the
  commit message and commits approved work.

Keeping the Reviewer alive across the user checkpoint is
why TeamCreate is used even for this single-agent case —
it allows the lead to send a "commit" message after user
approval rather than re-spawning a new agent.

## Flow

1. Lead reads relevant files to understand current state
2. Lead implements the change directly
3. Lead runs tests and linters if applicable — catching
   regressions before presenting to the Reviewer avoids
   wasted review cycles
4. Lead creates a one-agent team via TeamCreate with the
   Reviewer — Reviewer performs full review including
   CLAUDE.md drift detection. Even small changes can
   introduce drift
   (e.g., renaming a directory that CLAUDE.md references),
   and Direct-Review has the least process, making
   undetected drift most likely here.
5. If rejected: lead fixes issues and re-sends to Reviewer
6. **User checkpoint** — lead presents the completed work,
   Reviewer's summary, and proposed commit message for
   user approval
7. If approved, lead tells Reviewer to commit
8. If changes are needed, lead adjusts and returns to
   step 3

## Completion Criteria

- Change implemented as requested
- Tests pass (if applicable)
- Reviewer has approved the result (including drift check)
- User has approved the result
- Work committed by Reviewer
