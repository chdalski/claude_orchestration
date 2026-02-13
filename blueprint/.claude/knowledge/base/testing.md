# Testing Principles

## What Makes a Good Test

### Independence

- Each test must run in isolation
- No test should depend on another test's state or
  execution order
- Tests should set up their own preconditions and clean up
  after themselves

### Determinism

- Same inputs must always produce same results
- No reliance on external state, timing, or randomness
- Flaky tests erode confidence and must be fixed immediately

### Clarity

- Test names describe the behavior being verified, not the
  implementation
- One assertion per test when possible
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

### Focus

- Test behavior, not implementation details
- Tests should survive refactoring if behavior is unchanged
- Avoid testing private internals — test through the public
  interface

## Test Design

### Coverage Strategy

- Start with happy paths (expected usage)
- Add edge cases (boundaries, empty inputs, maximums)
- Add error conditions (invalid input, failures)
- Order from simple to complex to guide incremental
  development

### Naming

- Names should read as behavior specifications
- Pattern: `should_<expected_behavior>_when_<condition>`
- Bad: `test_calculate`, `test1`, `testError`
- Good: `should_return_zero_for_empty_input`,
  `should_reject_negative_values`

## Anti-Patterns

### Excessive Mocking

- Mocks that replicate implementation details make tests
  brittle
- Prefer real collaborators when practical
- Mock at system boundaries (network, filesystem, time)

### Implementation Coupling

- Tests that break when internals change but behavior stays
  the same
- Testing private methods directly
- Asserting on internal state instead of observable output

### Test Interdependence

- Shared mutable state between tests
- Tests that must run in a specific order
- Setup in one test that another test relies on

### Ignoring Warnings

- Compiler and type-checker warnings in test code matter
- Suppressing warnings hides real problems
- Treat test code with the same rigor as production code
