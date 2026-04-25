# Behavior-Preserving Cuts

The companion to `reasoned-instructions.md`. That rule
governs writing — when to *add* rationale (only when it
would change how an agent applies the instruction). This
rule governs review — when to *remove* existing prose
(only when removal would not change agent behavior).

Write-time biases toward inclusion ("err toward adding
context"). Review-time biases toward subtraction ("err
toward keeping files lean"). Together they balance: useful
rationale gets added, decoration gets pruned. Without the
review-side rule, files accumulate context that increases
file length — and length directly degrades adherence (the
`rule_file_length` ceiling exists for that reason).

## The Test

For a paragraph or sentence under review, ask: would
removing it change *any* of —

- which actions the agent takes,
- in what order,
- under what conditions,
- with what error handling?

If the answer to all four is no, the prose is decorative.
Cut it. If you cannot answer with confidence, the prose is
load-bearing in some way you have not yet identified —
keep it. The asymmetric cost favors keeping: a kept-but-
unnecessary paragraph costs marginal context; a wrongly-cut
paragraph costs a behavioral regression that may not
surface for weeks.

## False Positives

Four shapes look cuttable but are not. If your candidate
matches one of these, the cut is probably wrong. Each
example below is a real survey false positive from the
workflow blueprint's `CLAUDE.md`.

### Restatement of a different failure mode

> "Do not skip clarification for simple tasks..."
>
> "**Imperative commands are not workflow selections.** When
> a user says 'fix X', that is a statement of goal — it
> begins clarification, it does not end it."

Both paragraphs say "clarify before acting," but they
counter different rationalizations. The first targets
agents perceiving a task as too simple to clarify. The
second targets agents parsing imperative phrasing as a
direct execution instruction. A single rule about "always
clarify" wouldn't cover both.

**Check before cutting:** can you construct a failure case
the second paragraph catches that the first would not? If
yes, both are load-bearing.

### Section opening mistaken for restatement

> "## When the User Asks for a Plan Directly
>
> If the user requests a plan, do not enter plan mode
> yourself..."

A section's first directive is not a restatement of the
heading — it is the section's body. Cutting it leaves the
section without an entry point.

**Check:** does the prose appear under a heading that
names the same situation? Then it is the body, not a
duplicate. Keep.

### Operational prose disguised as rationale

> "Creating one team upfront is simpler — it ensures all
> agents can communicate via SendMessage from the start.
> Other agents idle during planning; this is expected."

The "simpler" framing reads as decorative. The clause
actually specifies a precondition (spawn the full team
before any messaging) and pre-empts an anti-pattern
(reactive incremental spawning). Without it, the agent
might spawn teammates as needed and break the
communication infrastructure.

**Check:** does the clause specify sequencing,
preconditions, operational constraints, or pre-empt a
specific anti-pattern? It is operational prose. Keep.

### "No exceptions" clauses

> "There are no exceptions — the Reviewer gate exists
> precisely because 'obvious' changes introduce regressions."

Looks like emphasis. Counters a specific bias: agents
naturally carve out cases for "tiny" or "obvious"
changes. Removing the clause leaves the directive but
removes its resistance to rationalization.

**Check:** does the prose explicitly counter an exception
the agent would otherwise self-grant? Keep.

## Genuine Candidates

Real cuts are smaller than they appear. The shapes that
actually pass the test:

- **Pure echoes** — "Use lowercase agent names. Naming
  consistency matters." The second sentence adds nothing.
- **Closing summaries** — "Remember:" sections that
  enumerate what the file just covered.
- **Connective tissue** — "It is important to note
  that...", "As described above..." preambles before
  content the reader already encounters.
- **Rule-echo parentheticals** — "Order tests simple →
  complex (because order matters)."

Bloat in agent-instruction files is mostly load-bearing.
This is a feature: the prose encodes failure modes the
rule alone would miss. Expect cuts to be measured in
single sentences across many files, not in paragraphs in
any one file.

## When to Apply

- Editing a file untouched for months — old rationale may
  have become echo as surrounding rules evolved.
- After a refactor that consolidates files — carryover
  content often duplicates new structure.
- During audits (see `blueprint-audit` skill).

Do not apply:

- During initial drafting — `reasoned-instructions.md`
  governs there. Add liberally; prune later.
- To cut concrete failure citations ("a prior session did
  X and broke Y"). These are `reasoned-instructions.md`
  keepers regardless of how decorative they may seem.

## Scope

All files agents read as instructions: `CLAUDE.md`,
`agents/*.md`, `skills/**/SKILL.md`, `rules/*.md`,
`workflows/*.md`. Not `README.md` (human-facing) or test
files.
