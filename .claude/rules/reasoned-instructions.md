# Reasoned Instructions

Blueprint markdown files are read by AI agents, not just
humans. An agent that understands *why* an instruction exists
will apply it correctly in novel situations, make better
trade-off decisions when instructions conflict, and avoid
cargo-culting rules that don't apply to the current context.
Instructions without rationale produce brittle compliance —
the agent follows the letter but misses the intent.

## The Rule

Every directive, constraint, or recommendation in a
blueprint markdown file must include its rationale. State
what to do, then state why.

## What "Include Rationale" Means

The rationale is a brief explanation — typically one or two
sentences — that answers "why does this rule exist?" or
"what goes wrong if this is ignored?" It sits directly after
or alongside the instruction, not in a separate section.

Good:

> Each test must run in isolation — shared mutable state
> between tests creates order-dependent failures that only
> surface in CI and are expensive to debug.

Weak:

> Each test must run in isolation.

The weak version tells the agent *what* to do but gives no
basis for judgment. When the agent encounters a case where
full isolation is costly (e.g., a database integration test),
it has no framework for deciding whether the trade-off is
acceptable.

## Scope

This applies to all files that agents consume as
instructions:

- `CLAUDE.md` files
- Agent definition files (`agents/*.md`)
- Knowledge files (`knowledge/**/*.md`)
- Practice files (`practices/*.md`)
- Rule files (`.claude/rules/*.md`)
- Templates (`templates/*.md`)

It does not apply to `README.md` files, which target human
readers and follow different conventions.

## Applying This Rule

When writing or editing a blueprint markdown file:

1. After each instruction, ask: "Would an agent who has
   never seen this codebase understand *why* this matters?"
   If the answer is no, add the rationale.

2. Keep rationale concise. One to two sentences is almost
   always enough. The goal is grounding, not persuasion.

3. When an instruction is a well-known engineering practice
   (e.g., "validate all external input"), the rationale
   should name the specific risk or failure mode, not just
   restate the instruction in different words.

4. When instructions may conflict in practice, the rationale
   helps agents resolve the tension. For example, "keep
   functions short" and "avoid premature abstraction" can
   pull in opposite directions — rationale clarifies which
   concern dominates and when.
