# TDD Blueprint (v1)

Test-driven development blueprint for Claude Code
multi-agent orchestration. The Test Engineer writes all
test code before the Developer implements.

## How It Works

### Testing Approach

The Test Engineer **owns all test code**. The Developer
owns source code only. This strict file ownership boundary
enforces that tests exist before implementation — the
Developer literally cannot start until the Test Engineer
delivers the test files.

### Workflow

1. All three dev-team agents receive the task and discuss
   approach.
2. Test Engineer writes all tests (unit + integration) in
   one batch, following the red-green-refactor TDD workflow.
3. Test Engineer sends "tests ready" to the Developer.
4. Developer implements source code to make the tests pass.
5. Security Engineer reviews throughout and sends
   post-implementation sign-off.
6. Dev-team reports completion to the lead.
7. Reviewer examines the work, commits if satisfied.

### Key Rules

- **Test Engineer goes first** — Developer waits for "tests
  ready" before writing any code.
- **All tests in one batch** — no phased test writing. The
  Developer gets the full picture before implementing.
- **Spike integration tests** — Test Engineer writes and
  runs one integration test to validate the harness before
  writing the full batch.
- **Split file ownership** — Test Engineer owns test files,
  Developer owns source files. For shared files (package
  manifest), Test Engineer edits first.

### Agents

| Agent | Role | Writes Code |
|-------|------|-------------|
| **Developer** | Source code | Yes (source only) |
| **Test Engineer** | Test code | Yes (tests only) |
| **Security Engineer** | Security review | No (advisory) |
| **Reviewer** | Quality gate | No (commits only) |

## Setup

```bash
cp -r .claude/ /path/to/your/project/.claude/
```

See the repository README for prerequisites and
configuration details.
