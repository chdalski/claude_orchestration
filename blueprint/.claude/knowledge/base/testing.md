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

- Create a list of test cases (marked as skipped/ignored)
  before writing any implementation
- Include the full scope: happy paths, edge cases,
  boundary conditions, error conditions
- This helps understand the complete expected behavior
- Order tests from simple to complex to guide incremental
  development

```pseudocode
tests:
    [skip] should_return_zero_for_empty_input
    [skip] should_return_number_for_single_input
    [skip] should_return_sum_for_two_numbers
    [skip] should_handle_negative_numbers
    [skip] should_reject_non_numeric_input
```

### 2. One Test at a Time

- Activate exactly ONE test at a time
- All other tests remain skipped
- Never have more than one failing test in the red phase
- Implement only what is needed to make that single test
  pass
- Don't think ahead or implement features for future tests

### 3. Red-Green-Refactor Cycle

#### Red Phase (Compilation/Type Error)

- Start with a non-existent function
- Test should fail with a compilation or type error
- This ensures we are truly starting from scratch

```pseudocode
test should_return_zero_for_empty_input:
    result = calculate([])  // function does not exist yet
    assert result == 0
```

#### Red Phase (Runtime Error)

- Create an empty function that returns a wrong value
- Test should fail with an assertion error
- This verifies our test is working as expected

```pseudocode
function calculate(numbers):
    throw "not implemented"  // or return wrong value
```

#### Green Phase

- Implement minimal code to make the test pass
- Don't add features for future tests
- Don't optimize or refactor yet

```pseudocode
function calculate(numbers):
    return 0  // simplest possible implementation
```

#### Refactor Phase

- MUST attempt at least one refactoring
- If no improvement is possible, document why

**Naming Evaluation (First Priority)**:

- Ask: "Does this name clearly describe what the function
  does based on all tests so far?"
- Ask: "Has the function's purpose become clearer through
  the latest test?"
- Rename if the name doesn't capture the current intent

**Apply APP (Absolute Priority Premise)**:

- Calculate mass before and after refactoring
- Aim for lower mass where possible
- Document mass changes
- See [code-mass.md](code-mass.md) for details

**Apply 4 Rules of Simple Design**:

- Tests must pass (Rule #1)
- Reveals intent (Rule #2)
- No duplication (Rule #3)
- Fewest elements (Rule #4)
- See [principles.md](principles.md) for details

**If no refactoring improves the code**:

- Document why no refactoring was possible
- Explain why the current state is optimal
- Move to the next test

### 4. Guessing Game

Before running tests, explicitly state:

- Which test will fail
- Type of error (compilation, assertion, panic)
- Expected vs actual values
- Expected error message

```text
Prediction:
- Test: should_return_sum_for_two_numbers
- Failure type: Assertion error
- Expected: 3
- Actual: 0
- Reason: Current implementation always returns 0
```

Run the test, then compare the actual result with your
prediction. This builds understanding of what you are
testing and why.

### 5. Baby Steps

- Make the smallest possible change to get to green
- If a test fails, make it pass with the simplest
  implementation
- Don't try to solve multiple problems at once
- Each step should be clear and verifiable

## Best Practices

### Test Structure

- One assertion per test when possible
- Clear, descriptive test names
- Tests should be independent
- No test should depend on another test's state
- Use the Arrange-Act-Assert pattern

```pseudocode
test order_id_rejects_negative_value:
    // Arrange
    input = -1

    // Act
    result = OrderId.new(input)

    // Assert
    assert result is Error(NegativeIdError)
```

### Implementation

- Start with the simplest possible implementation
- Don't add features until there is a test for them
- Don't optimize until all tests are green
- Keep the code clean and maintainable
- Use language-idiomatic patterns

### Documentation

- Tests serve as documentation
- Test names should describe the behavior
- Document mass calculations and refactoring decisions
- Document when no refactoring is possible

## Common Pitfalls

### 1. Writing Too Many Tests at Once

- Stick to one test at a time
- Don't implement multiple features simultaneously
- Activate only one skipped test

### 2. Skipping the Red Phase

- Always start with a failing test
- Don't write implementation before the test
- Verify the test fails for the right reason

### 3. Over-Engineering

- Don't add features without tests
- Don't optimize prematurely
- Avoid unnecessary abstractions
- See [principles.md](principles.md) for YAGNI (Rule #4)

### 4. Not Refactoring

- Take time to clean up code
- Remove duplication
- Improve readability
- Always attempt refactoring after the green phase
- Use APP to measure improvements

### 5. Testing Anti-Patterns

- Excessive mocking that hides real behavior
- Tests coupled to implementation details
- Ignoring compiler/type-checker warnings
- Crashing on errors instead of returning error types

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

// 3. Implement minimal solution
function sum(numbers):
    return 0  // hardcoded -- passes first test only

// 4. Refactor (if applicable)
// 5. Activate next test and repeat
```
