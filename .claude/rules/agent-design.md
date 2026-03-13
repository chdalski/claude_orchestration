# Agent Design Principle

Agent files and workflow files have distinct, non-overlapping
responsibilities. Mixing them breaks the composability that
makes blueprint agents reusable across workflows.

## The Principle

**Agent files** define role and capability.
**Workflow files** define coordination.

These must not be mixed — an agent that encodes workflow
assumptions becomes tightly coupled to a specific team
structure and cannot be reused without modification.

## What Belongs in Agent Files

- The agent's purpose and domain expertise — what it is
  and what it knows
- How the agent does its work — its process, checklist,
  and quality criteria
- Generic communication: "notify the requester," "wait for
  a task," "send findings to whoever requested the review"
- Tool usage and constraints

## What Does NOT Belong in Agent Files

- **Named teammates** — "send to Developer and Test
  Engineer." Named teammates are a workflow fact; the
  agent doesn't know who is on the team.
- **Sign-off sequences** — "wait for both TE and SE
  sign-offs before proceeding." Sequencing and gates are
  workflow facts.
- **Workflow-specific coordination steps** — "report to
  Architect via TaskUpdate, then SendMessage." Which agents
  exist and how they connect is defined by the workflow.
- **Workflow conditionals** — "if this is a Direct-Review
  task…." Agents operate the same way regardless of which
  workflow invoked them.

## Why

A workflow file defines the team. If an agent re-defines
it — by naming teammates, encoding sequences, or branching
on workflow context — the agent breaks the moment a workflow
uses a different composition. The same agent should be
usable in any workflow without modification; the workflow
file is the single source of truth for team structure.

## The Communication Pattern

Use **"the requester"** for whoever initiated the agent's
current task. Use **"the implementor"** for whoever did
the work being reviewed. Never use role-specific names in
agent files — those are workflow facts, not agent facts.
The agent doesn't know which role sent the task; it only
knows it received one.

## Agent Naming Convention

Agent `name:` fields in frontmatter must use lowercase,
hyphenated forms: `developer`, `test-engineer`,
`security-engineer` — not `Developer`, `Test Engineer`, or
`Security Engineer`. This exists because `SendMessage`
requires exact name matching and agents naturally guess
hyphenated lowercase forms. When registered names used
title case with spaces (e.g., `Test Engineer`), agents
guessed `test-engineer`, messages were silently dropped,
and handoffs stalled for minutes with no error feedback.
Aligning registered names with the form agents guess
eliminates this mismatch at the source.

Agent filenames already follow this convention
(`test-engineer.md`). The `name:` field must match.

## Scope

This principle applies to all agent files in all blueprints
in this repository. When editing or creating an agent
definition, verify that no workflow-specific information
has been added.
