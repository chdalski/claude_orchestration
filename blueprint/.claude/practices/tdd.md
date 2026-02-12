# Test-Driven Development (TDD)

## TDD Discipline

TDD will feel counterintuitive:

- **Hardcoded returns feel wasteful** -- but they are the
  correct minimal step
- **The urge to implement ahead is strong** -- resist it
- **Minimal steps feel slow** -- but they accelerate
  development
- **Refactoring feels optional** -- it is mandatory

Common violations:

- Multiple active tests at once
- Implementing beyond what tests demand
- Skipping the refactor phase
- Premature abstraction

**Remember**: Discomfort signals you are doing it right.
Trust the process.

## Core TDD Process

### 1. Test List First

Before writing any implementation, create a list of test
cases marked as skipped/pending/ignored:

- Include the full scope: happy paths, edge cases,
  boundary conditions, and error conditions
- Order tests from simple to complex to guide incremental
  development
- This helps understand the complete behavior expected
  from the code

```pseudocode
test suite "Calculator":

    // Happy path tests
    [skip] test should_return_zero_for_empty_input
    [skip] test should_return_number_for_single_input
    [skip] test should_return_sum_for_two_numbers

    // Edge cases and error conditions
    [skip] test should_handle_negative_numbers
    [skip] test should_reject_non_numeric_input
```

### 2. One Test at a Time

- Activate exactly ONE test at a time
- All other tests remain skipped
- Never have more than one failing test in red phase
- Implement only what is needed to make that single test
  pass
- Do not think ahead or implement features for future tests

### 3. Red-Green-Refactor Cycle

#### Red Phase (Compilation/Syntax Error)

- Start with a non-existent function
- Test should fail because the function does not exist
- This ensures we are truly starting from scratch

```pseudocode
test should_return_zero_for_empty_input:
    // Function does not exist yet
    result = calculate([])
    assert result equals 0
```

#### Red Phase (Runtime Error)

- Create an empty function that returns a wrong value
  or throws
- Test should fail with an assertion error
- This verifies our test is working as expected

```pseudocode
function calculate(numbers: list of int) -> int:
    throw NotImplementedError
    // or: return -1 (wrong value)
```

#### Green Phase

- Implement minimal code to make the test pass
- Do not add features for future tests
- Do not optimize or refactor yet

```pseudocode
function calculate(numbers: list of int) -> int:
    return 0  // Simplest possible implementation
```

#### Refactor Phase

MUST attempt at least one refactoring. If no improvement
is possible, document why.

**Naming Evaluation (First Priority)**:

- Ask: "Does this name clearly describe what the function
  actually does based on all tests so far?"
- Ask: "Has the function's purpose become clearer or more
  specific through the latest test?"
- Rename if the name does not capture the current full
  intent

**Apply Four Rules of Simple Design**:

- Tests must pass (Rule 1)
- Reveals intent (Rule 2)
- No duplication (Rule 3)
- Fewest elements (Rule 4)
- See [principles.md](../knowledge/base/principles.md)
  for details

**If no refactoring improves the code**:

- Document why no refactoring was possible
- Explain why current state is optimal
- Move to next test

### 4. Guessing Game

Before running tests, explicitly state:

- Which test will fail
- Type of error (compilation/assertion/runtime)
- Expected vs actual values
- Expected error message or assertion output

Example prediction:

```text
Prediction:
- Test: should_return_sum_for_two_numbers
- Failure type: Assertion error
- Expected: 3
- Actual: 0
- Reason: Current implementation always returns 0
```

Run the test, then compare actual result with prediction.
This builds understanding of the code and catches
misconceptions early.

### 5. Baby Steps

- Make the smallest possible change to get to green
- If a test fails, make it pass with the simplest
  implementation
- Do not try to solve multiple problems at once
- Each step should be clear and verifiable

## Best Practices

### 1. Test Structure

- One assertion per test when possible
- Clear, descriptive test names
- Tests should be independent
- No test should depend on another test's state
- Use the Arrange-Act-Assert pattern

### 2. Implementation

- Start with the simplest possible implementation
- Do not add features until there is a test for them
- Do not optimize until all tests are green
- Keep the code clean and maintainable
- Use language idioms appropriately

### 3. Documentation

- Tests serve as documentation
- Test names should describe the behavior
- Document refactoring decisions
- Document when no refactoring is possible

## Common Pitfalls to Avoid

### 1. Writing Too Many Tests at Once

- Stick to one test at a time
- Do not implement multiple features simultaneously
- Activate only one skipped test at a time

### 2. Skipping the Red Phase

- Always start with a failing test
- Do not write implementation before test
- Verify the test fails for the right reason

### 3. Over-Engineering

- Do not add features without tests
- Do not optimize prematurely
- Avoid unnecessary abstractions
- See [principles.md](../knowledge/base/principles.md)
  for YAGNI (Rule 4)

### 4. Not Refactoring

- Take time to clean up code
- Remove duplication
- Improve readability
- Always attempt refactoring after green phase

## Example Workflow

```pseudocode
// 1. Create test list (all skipped)
test suite "Sum":
    [skip] test should_return_zero_for_empty_list
    [skip] test should_return_number_for_single_element
    [skip] test should_return_sum_of_two_numbers

// 2. Activate first test
test should_return_zero_for_empty_list:
    assert sum([]) equals 0

// 3. Implement minimal solution
function sum(numbers: list of int) -> int:
    return 0  // Hardcoded -- passes first test only

// 4. Refactor (if applicable)
// 5. Activate next test and repeat
```
