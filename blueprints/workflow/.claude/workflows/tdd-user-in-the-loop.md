# TDD User-in-the-Loop

<!-- SYNC NOTE: The Handoff Protocol section (Team Roster,
     Acknowledgment Rule, Lead-Monitored Transitions) and
     Flow steps 1–2 ("Architect sends task" and "Dev-team
     discusses the task") are shared verbatim with
     develop-review-supervised.md and
     develop-review-autonomous.md. When editing those
     sections, update the other two files as well.
     Note: the TDD Cycles (steps 5–11) and Sign-offs
     (steps 12–13) are TDD-specific and do not sync. -->

## When to Use

Use this workflow when the user wants fine-grained control
over the development process — specifically, visibility and
approval at every phase of test-driven development
(Red-Green-Refactor). It is appropriate when:

- The user wants to be in the loop when tests are created
  and when code is written to satisfy them
- The task benefits from incremental, disciplined TDD where
  each test is written, failed, passed, and refactored
  before moving to the next
- The user values correctness confidence over speed — this
  workflow is slower than the Develop-Review variants
  because it stops for user approval at every phase
  transition
- The codebase is unfamiliar or the task involves subtle
  logic where assumptions need frequent validation

Not appropriate when speed is the priority, when the user
trusts the team to batch work autonomously, or for non-code
tasks. Use Develop-Review (Supervised or Autonomous) instead
when the user does not need per-phase control — they produce
the same quality with fewer interruptions.

## Agents

### Workflow-Specific

| Agent | Role |
|-------|------|
| **Architect** | Reads the codebase, writes plans, decomposes into task slices, and feeds tasks to the dev-team sequentially. Collects completion signals and sequences the next task. |
| **Developer** | Implements all code (source + tests). Receives one phase instruction at a time from the lead (Red, Green, or Refactor) and executes only that phase. Does not advance to the next phase autonomously. |
| **Test Engineer** | Advisory — designs the full test list upfront, verifies each test as the Developer writes it, and provides post-implementation sign-off after all cycles complete. Does not write code. |
| **Security Engineer** | Advisory — provides pre-implementation security assessment and post-implementation sign-off. Does not write code. |
| **Reviewer** | Independent quality gate — evaluates the completed task for correctness, security, test coverage, design, and idioms. Composes the commit message and commits approved work after the user checkpoint. |

## Team Lifecycle

The lead creates one team via `TeamCreate` with all
workflow agents at workflow start. The team persists
across all task slices — re-spawning per task incurs
startup cost and breaks `SendMessage` communication.

## Handoff Protocol

Peer-to-peer `SendMessage` between team agents is
unreliable — messages are silently dropped if the sender
uses an incorrect agent name (e.g., `test-engineer` instead
of `Test Engineer`), and `SendMessage` returns success when
a message is queued, not when it is delivered. Senders have
no way to detect failed delivery, which causes stalls that
require lead intervention.

### Team Roster

The Architect includes the exact registered agent names in
every task message so agents know how to address each other:

```
Team roster (use these exact names in SendMessage):
- developer
- test-engineer
- security-engineer
- reviewer
```

Agents must use these names exactly as shown — lowercase,
hyphenated where multi-word. This convention exists because
agents naturally guess hyphenated lowercase forms; using
those as registered names eliminates the mismatch that
causes silent message loss.

### Acknowledgment Rule

When an agent receives a handoff message (task assignment,
completed work, verification request, sign-off), it must
reply with a brief acknowledgment via `SendMessage` to the
sender within 60 seconds. A simple "received, starting
verification" suffices. Without acknowledgment, the sender
cannot distinguish "processing" from "never received" — and
the resulting stall is invisible until the lead notices.

### Lead-Monitored Transitions

At certain handoff points, silent message loss causes the
longest stalls because the sender idles waiting for a
response that will never come. The lead proactively checks
for acknowledgment at these transitions:

- **Steps 12–13** — Test Engineer and Security Engineer send
  post-implementation sign-offs to Developer. The Developer
  is blocked until both arrive; a dropped sign-off stalls
  the entire task.
- **Step 17** — Reviewer sends rejection findings to
  Developer, Test Engineer, and Security Engineer

If no acknowledgment arrives within 2 minutes of a
monitored transition, the lead relays the message directly
to the recipient. This adds one message hop but eliminates
multi-minute stalls from undetected message loss.

## Flow

### Per Task Slice

#### Setup

1. **Architect sends task** to Developer, Test Engineer,
   and Security Engineer simultaneously — all three need
   the full task context to discuss the approach. Task
   descriptions must present the problem and context, not
   prescribed security mitigations — the Security Engineer
   performs independent threat modeling in step 2.

2. **Dev-team discusses the task.** Security Engineer
   broadcasts a pre-implementation security assessment to
   Developer and Test Engineer — OWASP categories, what
   the Test Engineer should cover, what the Developer
   should watch for. This assessment is independent — the
   Security Engineer evaluates the full threat model, not
   just mitigations suggested in the task description.

3. **Test Engineer produces the test list** — a structured
   specification of every test case, ordered from simple
   to complex — and sends it to the Developer and the
   lead. The ordering matters because TDD builds
   complexity incrementally; simple tests drive out the
   core design before edge cases add conditional logic.

4. **User checkpoint — test list approval.** The lead
   presents the test list to the user. The user may
   approve, modify, add, or remove test cases. The lead
   relays any changes to the Test Engineer and Developer.
   This checkpoint exists because the user explicitly
   wants to be in the loop when tests are created — the
   test list defines what the code will do, so approving
   it is approving the specification.

#### TDD Cycles (steps 5–11, repeated per test)

The **lead controls the phase loop** — the Developer
receives one phase instruction at a time and must not
proceed to the next phase autonomously. This structural
enforcement exists because a Developer that receives the
full test list and a "do TDD" instruction will optimize
by collapsing phases, writing tests and implementation
together, or skipping refactoring. Sending one phase at
a time makes it structurally impossible to skip ahead.

For each test case in the approved test list:

5. **Lead sends Red phase instruction** to the Developer
   via `SendMessage`. The message must be explicit:

   > **Phase: RED** — Write one failing test for: [test
   > case description from the approved list]. Write
   > only the test — no implementation code. Run the
   > test, confirm it fails, and report back with:
   > (1) the test code, (2) the failure output. Do not
   > proceed to Green.

   The Developer writes the test, runs it, confirms
   failure, and sends the test code and failure output
   back to the lead. The Developer does nothing else —
   no implementation, no other tests.

   **Failed prediction:** If the test passes unexpectedly
   (the behavior already exists), the Developer stops
   and messages the lead immediately. The lead consults
   the user — this may indicate the test list needs
   updating, the behavior was already implemented in a
   prior cycle, or the test is not asserting what was
   intended. Do not proceed until the user decides how
   to handle it.

6. **User checkpoint — Red phase.** The lead presents the
   failing test and its output to the user. The user
   confirms the test is correct and approves moving to
   the Green phase. This checkpoint lets the user verify
   that the test matches their intent before any
   implementation happens.

7. **Lead sends Green phase instruction** to the Developer
   via `SendMessage`:

   > **Phase: GREEN** — Write the minimum code needed to
   > make the failing test pass. All existing tests must
   > also continue to pass. "Minimal" means the simplest
   > code that satisfies the assertion — hardcoded
   > returns are acceptable. Do not refactor, do not
   > generalize, do not add code for future tests. Run
   > all tests, confirm they pass, and report back with:
   > (1) the implementation code, (2) the test output.
   > Do not proceed to Refactor.

   The Developer implements, runs all tests, and sends
   the implementation and test output back to the lead.

   **Failed prediction:** If any previously passing test
   now fails, the Developer stops and messages the lead.
   The lead consults the user — the new implementation
   broke an assumption from an earlier cycle. Do not
   proceed until the regression is resolved.

8. **User checkpoint — Green phase.** The lead presents
   the implementation and passing test output to the
   user. The user confirms the implementation is
   acceptable and approves moving to the Refactor phase.

9. **Lead sends Refactor phase instruction** to the
   Developer via `SendMessage`:

   > **Phase: REFACTOR** — Attempt at least one
   > refactoring. Evaluate naming first, then look for
   > duplication, structural improvements, and
   > simplification opportunities. Run all tests after
   > each change to confirm they still pass. Report back
   > with: (1) what was changed and why, or why a
   > refactoring was attempted and rejected, (2) the
   > refactored code, (3) the test output. Do not
   > proceed to the next test.

   Mandatory refactoring after every Green phase is core
   TDD discipline — skipping it lets design debt
   accumulate across cycles until the code becomes
   difficult to extend.

   **Failed prediction:** If any test fails after
   refactoring, the Developer reverts the refactoring
   change and messages the lead. Refactoring must not
   change behavior — a failing test means the
   refactoring was incorrect.

10. **User checkpoint — Refactor phase.** The lead
    presents the refactored code and passing test output
    to the user. The user approves moving to the next
    test.

11. **Test Engineer verifies the test.** After user
    approval of the cycle, the Test Engineer reads the
    test file, confirms the test matches its
    specification from the test list (name, scenario,
    assertions), and sends confirmation to the lead.
    This incremental verification catches spec drift
    early — without it, mismatches accumulate across
    cycles and require a costly batch correction at the
    end.

**Repeat steps 5–11** for each test case in the approved
test list. The lead must send a new phase instruction
for each step — the Developer never receives more than
one phase at a time.

#### Sign-offs

12. **Test Engineer post-implementation sign-off.** After
    all TDD cycles are complete, the Test Engineer reads
    all test files and confirms: every test from the
    approved list exists, no tests were skipped or
    weakened, and all tests pass. Sends sign-off to
    Developer.

13. **Security Engineer post-implementation sign-off.**
    The Security Engineer reviews the complete
    implementation — all source and test files written
    during the TDD cycles. Checks for vulnerabilities,
    missing input validation, auth gaps. Sends sign-off
    to Developer.

14. **Developer reports implementation complete** to
    Architect — having received both sign-offs, sends a
    summary via SendMessage.

15. **Architect messages lead** that the task is ready
    for review.

### Review

16. **Lead sends to Reviewer** — include the task
    description and acceptance criteria from the plan so
    the Reviewer can verify scope completeness. Without
    the task context, the Reviewer can only evaluate code
    quality, not whether every requested feature was
    delivered. Reviewer evaluates scope completeness,
    correctness, security, test coverage, design, and
    language idioms.

17. **If rejected:** Reviewer sends specific findings to
    Developer, Test Engineer, and Security Engineer. All
    three receive findings so they can coordinate the
    fix. Developer fixes. Return to step 12 — both
    sign-offs are required again after fixes, because
    changes during a fix can introduce new issues.

18. **If approved:** Reviewer reports approval to lead
    with review summary, proposed commit message, and
    file list.

### Commit

19. **User checkpoint — commit approval.** The lead
    presents the completed work, Reviewer's summary, and
    proposed commit message to the user. Even though the
    user approved each phase individually, this final
    checkpoint covers the aggregate — the user sees the
    full changeset before it enters git history.

20. **Lead tells Reviewer to commit.** Reviewer stages
    the files and commits with the prepared message,
    reports the short SHA to the lead. Lead tells Architect
    the task is committed. Architect marks the task
    completed via TaskUpdate, updates the plan file, and
    feeds the next task slice (loop to step 1).

## Completion Criteria

The workflow is complete when:

- All task slices from the Architect's plan are committed
- Each test in every test list went through a complete
  Red-Green-Refactor cycle with user approval at each
  phase transition
- Refactoring was attempted after every Green phase
- Each slice received both Test Engineer and Security
  Engineer sign-offs before review
- Each slice passed Reviewer approval before commit
- All tests pass across the full project after the final
  commit
- The user approved each commit at the commit checkpoint
