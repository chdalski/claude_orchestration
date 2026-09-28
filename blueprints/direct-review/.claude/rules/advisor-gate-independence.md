# Advisor Gate Independence

A Security-Hybrid task (see `risk-assessment.md`) has two
Security Engineer gates. Each gate is satisfied only by its
own explicit deliverable — no other message stands in for
it.

## The Gates

- **Pre-implementation gate** — a security assessment
  authored by the Security Engineer, ending in an explicit
  pre-implementation sign-off, received before any
  implementation edit.
- **Post-implementation gate** — the Security Engineer's
  explicit post-implementation sign-off on the final
  security-relevant diff and its quality-check results.

## What Does Not Count

- **A Reviewer approval.** The Reviewer checks quality and
  scope; it cannot satisfy either security gate.
- **A generic "security-engineer signed off."** The status
  must confirm the pre- and post-implementation sign-offs
  separately — a single sign-off cannot be told apart from
  a pre-sign-off reused as a post-sign-off.
- **The pre-implementation sign-off reused as the post-
  implementation one.** The pre-gate assessed a plan; the
  post-gate assesses code. Neither covers the other.
- **A post-implementation sign-off that predates the final
  diff.** A later change to production code or
  security-relevant configuration requires a fresh one.
  Two kinds of change do not: formatter output (the
  reviewer runs the formatter before approving) and a
  documentation change that does not alter policy or
  security behavior.
- **An unsolicited Security Engineer message.** If it does
  not answer a gate request for the current task, it is
  informational context, not a gate response.
- **A prior task's sign-off or an advise-mode
  consultation.** Each task gets its own gates. An
  advise-mode consultation weighed options before any plan
  existed; it assessed no concrete diff.

## How to Apply

### For implementors

Request each gate explicitly, naming the deliverable
expected ("pre-implementation sign-off for <task>",
"post-implementation sign-off for <task>"). The handoff to
the reviewer states both sign-offs separately.

### For reviewers

Verify the handoff cites both gates separately. A handoff
that claims one gate "was covered" by the other or by any
message listed above is grounds for rejection — send it
back for the missing explicit sign-off.

## Related Rules

- `risk-assessment.md` determines whether the gates apply.
- `procedural-fidelity.md` — each gate is a numbered step;
  skipping one because another "covers it" is a
  sufficiency fallacy.
