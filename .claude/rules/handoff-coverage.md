# Handoff Coverage Analysis

When designing or modifying a multi-agent pipeline in a
blueprint, verify that every property the pipeline should
guarantee has a responsible agent with sufficient input.
Gaps in this coverage are invisible during normal operation
— each agent does its job correctly, but the overall
pipeline silently drops a guarantee because no agent owns
it.

## The Problem

Multi-agent pipelines distribute verification across
agents. Each agent checks what it can see. When a property
falls between agents — agent A doesn't check it because
it assumes agent B will, and agent B lacks the information
to check it — the property goes unverified. These gaps
only surface when a real task hits the uncovered case,
often long after the blueprint was deployed.

Example: a reviewer evaluates code quality but never
receives the task description, so it cannot verify that
the delivered code covers the full requested scope. The
lead trusts the reviewer's approval without checking scope
itself. Result: partial delivery is approved and marked
complete.

## When to Apply

Run this analysis when:

- Creating a new multi-agent pipeline (new blueprint or
  new workflow within an existing blueprint)
- Adding, removing, or changing an agent's responsibilities
- Modifying what information is passed at a handoff point
- Adding a new guarantee the pipeline should provide

## How to Analyze

### Step 1: List the guarantees

Write down every property that should hold when the
pipeline completes a unit of work. These typically include:

- Code correctness (logic, no regressions)
- Test coverage (new behavior has tests)
- Scope completeness (all requested work was delivered)
- Security (no new vulnerabilities introduced)
- Commit hygiene (correct files staged, accurate message)
- Documentation accuracy (docs reflect the change)
- Plan fidelity (plan status reflects reality)

This list varies by blueprint. Add properties specific to
the pipeline's purpose.

### Step 2: For each guarantee, answer two questions

**Who verifies this?** Identify the specific agent and the
specific step in its instructions. If the answer is
"nobody explicitly" or "the lead, implicitly," that is a
gap. Implicit ownership means no agent will reliably
perform the check.

**Does that agent receive the necessary input?** Trace
the information the agent needs back to its source. If the
information originates in a different agent (e.g., the
plan lives with the lead, but the reviewer needs it),
verify that the handoff message carries it. An agent
cannot verify what it cannot see.

### Step 3: Record the results

A simple table is sufficient:

| Guarantee | Verifier | Step | Has input? |
|-----------|----------|------|------------|
| Code correctness | Reviewer | reads diff | Yes |
| Scope completeness | ??? | — | — |

Empty or uncertain cells are the gaps to fix.

## Fixing Gaps

When a gap is found, prefer the fix that places the check
where the information already exists — this avoids adding
new handoff complexity. If no agent has the information,
the cheapest fix is usually to include it in an existing
handoff message rather than adding a new communication
channel.

Avoid creating duplicate verification (two agents both
checking the same property) — this creates unclear
ownership and the same "someone else will catch it"
assumption that causes gaps in the first place. One agent
owns each guarantee.

## Common Gap Patterns

- **Scope vs. quality split:** One agent checks code
  quality, another owns the task plan, neither checks
  that the code delivers the full task scope.
- **Advisory gaps:** Advisors are consulted conditionally.
  If the trigger condition is too narrow, certain risks
  go unreviewed. Verify that trigger criteria match the
  actual risk surface.
- **Post-approval drift:** An agent approves work, then a
  later agent modifies state (reformats, updates docs)
  without re-verification. The approval covers a
  different state than what was committed.
- **Self-reported completeness:** An agent reports its own
  output as complete, and the next agent trusts the report
  without independent verification.
