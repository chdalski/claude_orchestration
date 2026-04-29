# Risk Assessment for Workflow Selection

This rule helps the lead assess whether a task requires the
Security Engineer and Test Engineer — which determines
whether Direct-Review is appropriate or the task must go
through a Develop-Review workflow.

In Develop-Review workflows, the Security Engineer and Test
Engineer are always included. The assessment here applies at
**workflow selection time** — specifically, whether
Direct-Review is safe for this task.

## High-Risk Indicators (Develop-Review Required)

If any of these apply, the task must not use Direct-Review —
it needs the Security Engineer's independent threat modeling:

- **Trust boundaries** — code that sits between trusted and
  untrusted contexts (e.g., parsing user-supplied input,
  handling authentication/authorization)
- **Untrusted input** — deserialization, schema validation,
  file path handling, URL parsing from external sources
- **Cryptographic operations** — key management, token
  generation, signature verification, hashing
- **Network-facing code** — HTTP handlers, WebSocket
  endpoints, API routes exposed to clients
- **Secrets handling** — configuration that touches
  credentials, tokens, API keys, connection strings
- **Permission/access control** — code that decides what
  users can see or do
- **Data persistence** — SQL queries, file writes, cache
  operations where injection or corruption is possible

## High-Uncertainty Indicators (Develop-Review Recommended)

If any of these apply, the task benefits from the Test
Engineer's structured test design:

- Design trade-offs to evaluate — multiple valid approaches
  make it unclear which behaviors to assert
- Complex interactions between components — integration
  points where failures are subtle and hard to predict
- Greenfield code with no existing test patterns — no
  existing tests to follow as examples
- The task adds or modifies public API surface — API
  contracts need explicit coverage because callers depend
  on them

## Low-Risk Indicators (Direct-Review Eligible)

Direct-Review is appropriate only when the task meets both
Direct-Review criteria (no security ramifications, tests
already cover it or none needed) and matches these
characteristics:

- **Pure functions** — no I/O, no side effects, no external
  input
- **Internal wiring** — module registration, capability
  flags, handler delegation to existing functions
- **Pattern-following** — code structurally identical to
  existing, reviewed code in the same codebase
- **Test-only changes** — adding or modifying tests without
  changing production code
- **Refactoring** — restructuring code without changing
  behavior or trust boundaries
- **Documentation** — comments, README updates, plan files

## Do Not Prescribe Security Mitigations

When writing the plan, or when implementing directly in
Direct-Review, do not include security mitigations in the
task description (e.g., "use bcrypt for hashing," "limit
input length to 1024 chars as ReDoS guard"). If you
identify a security concern, that is a signal to route
the task through Develop-Review where the Security
Engineer handles it — not a signal that you have
sufficient expertise to specify the controls.

Prescribed mitigations anchor downstream agents: the
Security Engineer validates what was suggested instead of
performing independent threat modeling, and the Developer
treats the mitigations as sufficient coverage. A production
incident showed that lead-prescribed mitigations ("limit
pattern length as ReDoS guard") missed three additional
issues that the Security Engineer's independent assessment
later identified. Surface-level mitigations create a false
sense of coverage.

The lead identifies risk categories. The Security Engineer
specifies controls. These roles must not be mixed.

## When in Doubt, Choose Develop-Review

The cost of including the Security Engineer on a task that
didn't need it (a few extra messages) is far lower than the
cost of routing a security-sensitive task through
Direct-Review where no independent assessment occurs.
