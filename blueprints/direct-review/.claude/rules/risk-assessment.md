# Risk Assessment

This rule is the single normative source for classifying a
task before implementation. The lead applies it to every
plan task before its first edit, and when weighing options
in advise mode. Classification selects one of three paths.

## Reviewer-Only

Eligible only when the task has no security ramifications
and one of these applies:

- Existing tests exercise the changed production entry
  point and assert the behavior being changed.
- The change is a behavior-preserving refactor, and tests
  that pass before it exercise the behavior it preserves —
  existing ones, or ones a preceding task added to pin it.
- The change only adds tests for existing behavior.
- The change is non-behavioral documentation, comment, or
  formatting work and needs no test.

The Reviewer is the only gate.

## Security-Hybrid

Required for security-relevant work that has no escalation
trigger below. A task is security-relevant when it touches
any of:

- A trust boundary — code between trusted and untrusted
  contexts
- Untrusted input — parsing, deserialization, schema
  validation, file path or URL handling
- Cryptographic operations or secrets handling
- Network-facing code — HTTP handlers, WebSocket
  endpoints, API routes
- Permission or access-control logic
- Data persistence — SQL, file writes, cache operations
- Configuration touching any of the above, even a
  one-line change

Some of these areas also appear as escalation triggers
below; a trigger takes precedence. The Security Engineer
gives an explicit pre-implementation sign-off before any
edit and an explicit post-implementation sign-off on the
final diff; the Reviewer remains the final quality gate.

Existing HTTP and DB read/write paths, static parameterized
queries, limited database migrations, and parsing, mapping,
serialization, or data-integrity changes are Security-Hybrid
work when no trigger applies. Network, persistence, or API
contact alone is not a trigger.

## Escalate to the User

Stay in advise mode — make no implementation edit — when a
task has either of these:

1. **A high-risk category:**
   - Authentication, authorization, or permission/access
     decisions
   - Secrets, credentials, tokens, or cryptographic
     operations
   - A new or widened external input source or accepted
     input form
   - Dynamic SQL, identifiers, file paths, URLs, commands,
     or templates constructed from untrusted data
   - A possible effect beyond the current operation and data
     scope: another user, tenant, data scope, permission,
     confidential data, or code execution
2. **A behavioral change no existing test covers**, with no
   security ramifications otherwise.

Name the trigger and the affected input, operation, or data
scope, then ask the user to choose explicitly:

- **Proceed with Security-Hybrid anyway.** For trigger 2,
  the plan must add tests that exercise the changed entry
  point, and the Reviewer verifies them against the plan.
- **Handle the task outside this blueprint.**

This blueprint has no separate developer and test-advisor
pipeline for these tasks, so the lead cannot compensate on
its own. Proceeding silently would give high-risk work less
scrutiny than the user expects; the choice is the user's,
not the lead's.

When the Security Engineer's pre-implementation assessment
reports a trigger the lead missed, stop and escalate the
same way before any implementation edit.

## When in Doubt

Classify upward: Security-Hybrid over Reviewer-only,
escalation over Security-Hybrid. An unnecessary security
review costs minutes; a missed one ships the vulnerability.

## Do Not Prescribe Security Mitigations

The lead identifies risk categories but does not prescribe
controls in plans, task descriptions, or advice. The
Security Engineer specifies controls during its assessment.
A prior incident showed that when the lead prescribed a
mitigation ("limit pattern length to ≤1024 chars as ReDoS
guard"), security was treated as addressed and the advisor
was never consulted; the advisor would have found three
further issues.
