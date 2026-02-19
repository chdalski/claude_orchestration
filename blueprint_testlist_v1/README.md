# Test-List Blueprint (v1)

Test-list-driven development blueprint for Claude Code
multi-agent orchestration. The Test Engineer designs what
to test, the Developer writes all code.

## How It Works

### Testing Approach

The Test Engineer is **advisory** — they produce a test
specification (what to test, not the test code) and verify
the Developer's tests match it. The Developer writes all
code: both source and tests. This unified ownership
eliminates file-conflict coordination and stop-start cycles
while preserving independent test design review.

### Workflow

1. All three dev-team agents receive the task and discuss
   approach.
2. Test Engineer produces a **test list** — a structured
   specification of every test case (scenarios, edge cases,
   expected outcomes).
3. Developer writes all tests from the spec in one batch.
   If integration tests are included, spikes one first to
   validate the harness.
4. Test Engineer **verifies** the written tests match the
   specification ("tests verified").
5. Developer implements source code to make the tests pass.
6. Test Engineer sends **post-implementation test sign-off**
   — confirms tests were not skipped, weakened, or removed
   during implementation.
7. Security Engineer sends post-implementation security
   sign-off.
8. Dev-team reports completion to the lead.
9. Reviewer examines the work, commits if satisfied.

### Key Rules

- **Test list before code** — Test Engineer produces the
  spec before the Developer writes anything. Test design
  stays independent from implementation.
- **Tests verified before implementation** — Developer sends
  written tests to the Test Engineer for verification
  before starting source code. Catches spec-to-test gaps
  early.
- **Dual post-implementation sign-offs** — both Test
  Engineer (test integrity) and Security Engineer (security
  concerns) sign off before the dev-team reports done. This
  exists because the Developer owns all code — without
  independent checks, tests could be weakened or security
  skipped under implementation pressure.
- **Spike integration tests** — Developer writes and runs
  one integration test first when the Test Engineer's spec
  includes them, to validate the harness before writing
  the full batch.

### Agents

| Agent | Role | Writes Code |
|-------|------|-------------|
| **Developer** | All code (source + tests) | Yes |
| **Test Engineer** | Test spec + verification | No (advisory) |
| **Security Engineer** | Security review | No (advisory) |
| **Reviewer** | Quality gate | No (commits only) |

## Setup

```bash
cp -r .claude/ /path/to/your/project/.claude/
```

Optionally, copy the devcontainer for sandboxed execution
with a network firewall and autopilot permissions:

```bash
cp -r .devcontainer/ /path/to/your/project/.devcontainer/
```

See the repository README for prerequisites, devcontainer
details, and configuration options.
