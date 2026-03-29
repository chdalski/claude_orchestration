---
paths:
  - "**/README*"
---

# Mermaid Diagrams in READMEs

Use Mermaid fenced code blocks instead of ASCII art for
flow diagrams, sequence diagrams, and architecture visuals
in README files — GitHub and most markdown renderers
display Mermaid natively, producing clearer visuals with
labeled edges, directional arrows, and subgroups that
ASCII cannot express.

Do not use Mermaid in `.claude/CLAUDE.md`, agent files, or
other files that agents consume as instructions ��� agents
read those as raw markdown and parse ASCII diagrams more
reliably than Mermaid DSL. README files are human-facing;
agent-facing files use ASCII when diagrams are needed.
