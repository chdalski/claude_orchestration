# TDD Workflow

This practice defines the step-by-step execution workflow
for Test-Driven Development. For test design principles
(structure, naming, anti-patterns), see
`knowledge/base/testing.md`.

## Mindset

TDD will feel counterintuitive:

- **Hardcoded returns feel wasteful** — but they are the
  correct minimal step
- **The urge to implement ahead is strong** — resist it
- **Minimal steps feel slow** — but they accelerate
  development
- **Refactoring feels optional** — it is mandatory

**Remember**: Discomfort signals you are doing it right.
Trust the process.

## Step 1: Create the Test List

Before writing any implementation, create all test cases
marked as skipped:

- Include the full scope: happy paths, edge cases,
  boundary conditions, error conditions
- Order from simple to complex
- This is the roadmap for the entire implementation

```pseudocode
tests:
    [skip] should_return_zero_for_empty_input
    [skip] should_return_number_for_single_input
    [skip] should_return_sum_for_two_numbers
    [skip] should_handle_negative_numbers
    [skip] should_reject_non_numeric_input
```

## Step 2: Activate One Test

- Activate exactly ONE test at a time
- All other tests remain skipped
- Never have more than one failing test
- Do not think ahead or implement features for future tests

## Step 3: Red-Green-Refactor

### Red Phase

Two sub-steps, each producing a different failure:

**Compilation/type error** — Start with a non-existent
function. The test fails because nothing exists yet.

```pseudocode
test should_return_zero_for_empty_input:
    result = calculate([])  // function does not exist yet
    assert result == 0
```

**Runtime/assertion error** — Create an empty function that
returns a wrong value. The test fails with an assertion
error, confirming the test actually checks something.

```pseudocode
function calculate(numbers):
    throw "not implemented"
```

### Green Phase

- Implement the minimal code to make the test pass
- Do not add features for future tests
- Do not optimize or refactor yet

```pseudocode
function calculate(numbers):
    return 0  // simplest possible implementation
```

### Refactor Phase

MUST attempt at least one refactoring. If no improvement
is possible, document why.

**Naming evaluation (first priority)**:

- Ask: "Does this name clearly describe what the function
  does based on all tests so far?"
- Ask: "Has the function's purpose become clearer through
  the latest test?"
- Rename if the name does not capture the current intent

**Apply APP (Absolute Priority Premise)**:

- Calculate mass before and after refactoring
- Aim for lower mass where possible
- Document mass changes
- See `knowledge/base/code-mass.md` for details

**Apply 4 Rules of Simple Design**:

- Tests must pass (Rule 1)
- Reveals intent (Rule 2)
- No duplication (Rule 3)
- Fewest elements (Rule 4)
- See `knowledge/base/principles.md` for details

**If no refactoring improves the code**:

- Document why no refactoring was possible
- Move to the next test

## Step 4: Baby Steps

- Make the smallest possible change to get to green
- If a test fails, make it pass with the simplest
  implementation
- Do not try to solve multiple problems at once
- Each step should be clear and verifiable

## Common Violations

- **Multiple active tests** — only one test should be
  unskipped at a time
- **Implementing beyond what tests demand** — write only
  enough code to pass the current test
- **Skipping the refactor phase** — refactoring is mandatory,
  not optional
- **Premature abstraction** — do not generalize until
  duplication forces it

## Example Workflow

```pseudocode
// 1. Create test list (all skipped)
tests:
    [skip] should_return_zero_for_empty_list
    [skip] should_return_value_for_single_element
    [skip] should_return_sum_for_multiple_elements

// 2. Activate first test
test should_return_zero_for_empty_list:
    assert sum([]) == 0

// 3. Run test — compilation error (sum does not exist)
// 4. Implement minimal solution
function sum(numbers):
    return 0  // hardcoded — passes first test only

// 5. Run test — passes
// 6. Refactor (if applicable)
// 7. Activate next test and repeat
```
