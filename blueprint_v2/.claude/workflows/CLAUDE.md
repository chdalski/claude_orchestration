# Workflow Format

Every workflow file in this directory defines a reusable
execution pattern. The lead reads these files to present
workflow options to the user. Keeping workflows as
separate files means adding a new workflow requires no
changes to CLAUDE.md or other configuration — just add
a file.

## Required Sections

### Name

A short, descriptive name. Use as the markdown heading —
the lead uses this name when presenting options to the
user.

### When to Use

Conditions where this workflow is the right choice:
- Task characteristics (size, complexity, risk)
- Team preferences (autonomy vs. control)
- Project context (new codebase, legacy, greenfield)

Be specific — the lead uses this section to match
workflows to tasks and explain trade-offs. Vague
conditions like "for complex tasks" don't help the lead
reason about which workflow fits.

### Agents

Which agents this workflow requires. Reference agent
names from `.claude/agents/` — this ensures the lead
spawns the right agents with the right tool sets and
instructions. For each agent, note its role in this
specific workflow, since the same agent may serve
different purposes in different workflows.

```markdown
- **Developer** — implements code and tests
- **Test Engineer** (advisory) — designs test spec,
  verifies coverage
```

### Flow

Step-by-step execution order. Number each step. Mark
handoff points between agents and user checkpoints
clearly — numbered steps prevent ambiguity about
ordering, and explicit checkpoints ensure the user
stays in control where it matters.

```markdown
1. Lead sends clarified task to Test Engineer
2. Test Engineer produces test spec
3. **User checkpoint** — review and approve test spec
4. Lead sends approved spec to Developer
5. Developer writes tests, then implements
6. Test Engineer verifies tests match spec
7. **User checkpoint** — review implementation
```

Use **User checkpoint** to mark where the user is
consulted. Use agent names to show who acts at each step.

### Completion Criteria

How to know the workflow is done. Be explicit — without
clear criteria, the lead has to guess when to stop,
which either cuts work short or wastes tokens on
unnecessary iterations.

```markdown
- All tests pass
- Test Engineer has given sign-off
- User has approved the final result
```

## Shared Agents

Some agents in `.claude/agents/` are not workflow-specific
— they provide utility functions that any workflow can use.
Workflow authors should use these rather than reinventing
their capabilities.

- **Architect** (`agents/architect.md`) — reads the
  codebase, writes plans, decomposes into vertical task
  slices, and feeds tasks to agents during execution. The
  lead spawns the Architect after clarification; it
  persists through both planning and execution phases.
  Workflows do not spawn the Architect — the lead does.
  During execution, the lead tells the Architect which
  agents the workflow provides, and the Architect feeds
  tasks to them sequentially via TaskList. Workflow authors
  should assume the Architect is available and define their
  agents and flow accordingly.

- **Committer** (`agents/committer.md`) — stages specified
  files and commits with a provided message. Use this
  agent whenever a workflow needs to commit work. The
  Committer is a mechanical executor: it does not review,
  judge, or modify content. Pass it the exact file list
  and commit message; it reports back with the SHA or an
  error. This keeps commit logic consistent across
  workflows and separates the "should we commit?" decision
  (the workflow's job) from the "execute the commit" action
  (the Committer's job).

- **Auditor** (`agents/auditor.md`) — checks CLAUDE.md
  structural claims against the filesystem. The lead
  spawns this at session start, not as part of a workflow.
  Listed here for awareness — workflow authors should not
  spawn the Auditor themselves.

## Conventions

- One workflow per file — mixing workflows in one file
  makes it harder for the lead to present individual
  options to the user.
- File names should be descriptive:
  `tdd-user-in-the-loop.md`, not `workflow-001.md` —
  the lead may scan file names to quickly identify
  candidate workflows.
- Keep workflows focused — a workflow that tries to
  cover every scenario is too broad to reason about,
  and the lead cannot clearly explain its trade-offs.
- Workflows reference agents but do not define them —
  agent definitions live in `.claude/agents/`. This
  separation means agent capabilities and workflow
  patterns evolve independently.
- The same agent can appear in multiple workflows with
  different roles — agents are general-purpose building
  blocks, workflows are specific compositions.
