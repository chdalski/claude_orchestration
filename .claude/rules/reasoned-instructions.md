# Reasoned Instructions

Blueprint markdown files are read by AI agents. Rationale
— the "why" after the "what" — helps agents apply
instructions correctly in situations the author didn't
anticipate. But not every instruction benefits equally.
A universal rationale mandate produces filler ("avoid
complexity because complexity is bad") that inflates file
length without changing agent behavior — and file length
directly degrades agent adherence.

## The Rule

Include rationale when it would change how an agent applies
the instruction. Skip it when the instruction is
unambiguous and has no edge cases.

## When Rationale Changes Behavior

### Non-obvious failure modes

The instruction exists because of a specific failure that
isn't predictable from the rule alone. Without the
rationale, an agent follows the letter but misses
structurally similar cases.

> Each step in this procedure must execute unconditionally
> — a prior session short-circuited after step 1 ("config
> found"), skipping the format-guide overwrite in step 2,
> and produced four plans against a stale template.

### Conflicting instructions

Two valid principles pull in opposite directions. Rationale
clarifies which dominates and when, giving the agent a
decision framework instead of an arbitrary choice.

> Extract common patterns (DRY), but not at the cost of
> clarity. Accidental similarity is not duplication — when
> removing duplication would create unclear abstractions or
> couple unrelated code, keep the duplication.

### Steps that appear skippable

An instruction looks redundant or optional but isn't.
Without rationale, an agent under optimization pressure
skips it.

> Run the formatter unconditionally before staging — not
> just `--check`. A check-fail-reformat cycle risks
> divergence between the working tree and staged changes,
> and the unconditional run is faster than the round-trip.

## When Rationale Is Overhead

Skip rationale for:

- **Simple mechanical rules** with no edge cases — "use
  lowercase hyphenated agent names" needs no explanation
  to follow correctly
- **Well-known engineering practices** where the model
  already has strong priors — "validate external input"
  is understood without restating the risk
- **Unambiguous directives** where no judgment call exists
  — if there's only one way to comply, rationale doesn't
  change compliance

When in doubt, err toward including rationale — a sentence
of useful context costs less than a misapplied rule. But a
sentence that restates the instruction in different words
costs tokens and dilutes signal.

## Applying This Rule

When writing or editing a blueprint markdown file:

1. After each instruction, ask: "Would an agent apply this
   differently if it understood why?" If yes, add rationale.
   If the instruction is unambiguous with no edge cases,
   the answer is usually no.

2. Keep rationale concise — one to two sentences. The goal
   is grounding, not persuasion.

3. Rationale should name the specific risk, failure mode,
   or trade-off — not restate the instruction in different
   words. "Avoid complexity because simple is better" is
   not rationale.

## Scope

This applies to all files that agents consume as
instructions: `CLAUDE.md` files, agent definitions
(`agents/*.md`), knowledge files (`knowledge/**/*.md`),
practice files (`practices/*.md`), rule files
(`.claude/rules/*.md`), and templates (`templates/*.md`).

It does not apply to `README.md` files, which target human
readers and follow different conventions.
