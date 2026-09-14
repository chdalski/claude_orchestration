---
paths:
  - "**/SKILL.md"
---

# Skills Must Conform to the Agent Skills Spec

Every skill in this repository must conform to the Agent
Skills specification. This applies to the project's own
audit skills (`/.claude/skills/`) and to blueprint skills
(`blueprints/*/.claude/skills/`) — the latter are copied
into target projects, so a non-conformant skill ships the
defect downstream.

**Source of truth:** the spec at
https://github.com/agentskills/agentskills (full text:
https://agentskills.io/specification). When the spec and
this rule disagree, the spec wins — update this rule.

**Validator:** `skills-ref validate ./<skill-dir>` checks
frontmatter and naming. Run it when available; it is the
authoritative check for the mandatory rules below.

## Mandatory (a skill is invalid without these)

A skill is a directory containing a `SKILL.md` file with
YAML frontmatter followed by a Markdown body.

- **`name`** (required): 1–64 characters; lowercase
  alphanumerics (`a-z`, `0-9`) and hyphens only; no
  leading or trailing hyphen; no consecutive hyphens.
  **Must match the parent directory name** — a mismatch
  breaks skill discovery and registration, and no error
  is surfaced when it happens.
- **`description`** (required): 1–1024 characters,
  non-empty.
- **Only these optional top-level keys are valid:**
  `license`, `compatibility` (≤500 chars), `metadata`
  (a map of string keys to string values), and
  `allowed-tools` (a space-separated string;
  experimental). Any other top-level frontmatter key is
  non-conformant. Note that `paths:` is a rule-file
  convention, not a skill field — never add it to a
  `SKILL.md`.

## Recommended (quality, not enforced by the validator)

- **`description` should state what the skill does *and*
  when to use it**, with concrete trigger keywords. The
  description is the only content loaded at startup when
  an agent decides whether to activate the skill; a pure
  "what" description with no "when" degrades
  auto-activation.
- **Keep `SKILL.md` under ~500 lines.** The entire body
  loads once the skill activates, so move detailed
  reference material into `references/` and let the agent
  pull it in on demand (progressive disclosure).
  Exception: a skill that executes all of its content on
  every run (e.g. an audit that runs every check) gains
  nothing from splitting — keep it cohesive. This is a
  recommendation, not a validation rule.
- **Keep file references one level deep** from `SKILL.md`,
  using relative paths. Optional subdirectories:
  `scripts/`, `references/`, `assets/`.

## When creating or editing a skill

1. Confirm `name` matches the directory and the format
   rules above.
2. Confirm `description` is non-empty, ≤1024 chars, and
   covers both what and when.
3. Confirm no non-spec top-level frontmatter keys.
4. If `SKILL.md` exceeds ~500 lines, split into
   `references/` unless the skill uses all of it each run.
5. Run `skills-ref validate ./<skill-dir>` if available.
