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

None workflow-specific. The lead handles all work directly.
The Committer is available for commits — separating commit
execution from implementation keeps the workflow consistent
with other workflows and avoids bundling git logic into the
lead's responsibilities.

## Flow

1. Lead reads relevant files to understand current state
2. Lead implements the change directly
3. Lead runs tests and linters if applicable — catching
   regressions before presenting to the user avoids
   wasted review cycles
4. **User checkpoint** — lead presents the completed work
   for review
5. If approved, lead spawns the Committer to stage and
   commit
6. If changes are needed, lead adjusts and returns to
   step 4

## Completion Criteria

- Change implemented as requested
- Tests pass (if applicable)
- User has approved the result
- Work committed via Committer
