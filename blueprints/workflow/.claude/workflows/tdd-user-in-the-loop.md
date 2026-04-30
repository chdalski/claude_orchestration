# TDD User-in-the-Loop

<!-- SYNC NOTE: The Handoff Protocol section (Team Roster,
     Acknowledgment Rule, Lead-Monitored Transitions) and
     Flow steps 1–2 ("Lead sends task" and "Dev-team
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

The lead includes the exact registered agent names in
every task message so agents know how to address each
other:

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
- **Step 16** — Reviewer sends rejection findings to
  Developer, Test Engineer, and Security Engineer

If no acknowledgment arrives within 2 minutes of a
monitored transition, the lead relays the message directly
to the recipient. This adds one message hop but eliminates
multi-minute stalls from undetected message loss.

## Flow

### Per Task Slice

#### Setup

1. **Lead sends task** to Developer, Test Engineer, and
   Security Engineer simultaneously — all three need the
   full task context to discuss the approach. Task
   descriptions must present the problem and context, not
   prescribed security mitigations — the Security Engineer
   performs independent threat modeling in step 2. Include
   the team roster (see Handoff Protocol above) so agents
   know how to address each other.

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

   > **Phase: RED** — For test case: [description from
   > the approved list]. Activate one pending placeholder
   > from the Minimum Required Tests and run two stages,
   > each gated by an explicit prediction:
   >
   > **Stage 1 — missing-symbol failure.** Write the test
   > calling the production symbol. Before running,
   > predict which symbol the runner cannot resolve and
   > what error it will produce (compile error,
   > ImportError, undefined identifier). Run the test;
   > confirm the actual failure matches the prediction.
   >
   > **Stage 2 — assertion failure.** Add the minimum
   > production-side stub to clear stage 1 (empty
   > function with the correct signature, returning a
   > default value — no logic). Before running, predict
   > the assertion failure: expected value vs. actual
   > value the stub returns. Run the test; confirm the
   > assertion failure matches the prediction.
   >
   > Report back: (1) test code, (2) both predictions,
   > (3) both failure outputs, (4) the stage-2 stub. Do
   > not write any logic in the stub. Do not proceed to
   > Green.

   The two-stage prediction discipline forces the
   developer to model both how the test fails to start
   and what it asserts before any logic is written —
   without it, "seeing red" carries no understanding of
   what red means.

   **Failed prediction.** If either prediction does not
   match the actual failure — wrong error type, wrong
   values, or the test unexpectedly passes — the
   Developer stops and messages the lead immediately.
   The lead consults the user. Wrong predictions are
   signals, not setbacks: they reveal that the
   developer's mental model does not match reality, the
   test list needs updating, the behavior is already
   implemented from a prior cycle, or the test is not
   asserting what was intended. Do not proceed until
   the user decides how to handle it.

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
   > each change to confirm they still pass. Compute APP
   > mass (per `code-mass.md`) before and after the
   > change — or state "mass unchanged" when the change
   > is purely naming. Report back: (1) what was changed
   > and why, or why a refactoring was attempted and
   > rejected, (2) the refactored code, (3) the test
   > output, (4) APP mass before / after. Do not proceed
   > to the next test.

   Mass before/after makes the trade-off observable to
   the reviewer: a refactoring that increases mass
   without a clarity gain is a regression dressed as
   improvement, and an unobserved mass change can
   silently push code past the rule's recommended
   thresholds.

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

14. **Developer reports implementation complete** to the
    lead — having received both sign-offs, sends a
    summary via `SendMessage`.

### Review

15. **Lead sends to Reviewer** — include the task
    description and acceptance criteria from the plan so
    the Reviewer can verify scope completeness. Without
    the task context, the Reviewer can only evaluate code
    quality, not whether every requested feature was
    delivered. Reviewer evaluates scope completeness,
    correctness, security, test coverage, design, and
    language idioms.

16. **If rejected:** Reviewer sends specific findings to
    Developer, Test Engineer, and Security Engineer. All
    three receive findings so they can coordinate the
    fix. Developer fixes. Return to step 12 — both
    sign-offs are required again after fixes, because
    changes during a fix can introduce new issues.

17. **If approved:** Reviewer reports approval to lead
    with review summary, proposed commit message, and
    file list.

### Commit

18. **User checkpoint — commit approval.** The lead
    presents the completed work, Reviewer's summary, and
    proposed commit message to the user. Even though the
    user approved each phase individually, this final
    checkpoint covers the aggregate — the user sees the
    full changeset before it enters git history.

19. **Lead tells Reviewer to commit.** Reviewer stages
    the files and commits with the prepared message,
    reports the short SHA to the lead. Lead updates the
    plan file (marks the task's checkboxes complete,
    records the commit SHA), then sends the next task
    slice (loop to step 1) or proceeds to plan completion
    if all slices are done.

## Completion Criteria

The workflow is complete when:

- All task slices from the approved plan are committed
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
