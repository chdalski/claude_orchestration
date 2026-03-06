# Solo

## When to Use

Use this workflow for trivial-to-small tasks (1-5 files,
mechanical or low-complexity changes) where the user
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
  CLAUDE.md drift detection. Spawned individually (via
  Agent tool, not TeamCreate) after the lead completes
  implementation, same pattern as the Committer.
- **Committer** — stages and commits files. Spawned
  individually after user approval.

Separating review and commit from implementation keeps Solo
consistent with other workflows and catches drift that a
single perspective would miss.

## Flow

1. Lead reads relevant files to understand current state
2. Lead implements the change directly
3. Lead runs tests and linters if applicable — catching
   regressions before presenting to the Reviewer avoids
   wasted review cycles
4. Lead spawns the Reviewer — Reviewer performs full review
   including CLAUDE.md drift detection. Even small changes
   can introduce drift (e.g., renaming a directory that
   CLAUDE.md references), and Solo has the least process,
   making undetected drift most likely here.
5. If rejected: lead fixes issues and returns to step 3
6. **User checkpoint** — lead presents the completed work
   and review summary for user approval
7. If approved, lead spawns the Committer to stage and
   commit
8. If changes are needed, lead adjusts and returns to
   step 3

## Completion Criteria

- Change implemented as requested
- Tests pass (if applicable)
- Reviewer has approved the result (including drift check)
- User has approved the result
- Work committed via Committer
