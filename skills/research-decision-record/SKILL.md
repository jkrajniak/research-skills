---
name: research-decision-record
description: Creates a dated ADR-style decision record for a parameter, baseline, or methodology choice that affects how results are interpreted. Use when a trade-off is made that a future reader or reviewer might question, or when a previous decision is superseded.
allowed-tools: [Read, Write]
---

# Research Decision Record

Creates a dated decision record (ADR-style) in `<proj>-research/decisions/`.

## When to use

- A parameter, baseline, or methodology choice affects how results are interpreted
- A trade-off was made that a future reader or reviewer might question
- A previous decision is superseded (create a new record referencing the old one)
- A scope change or deferral is made during revision

## Steps

### 1. Determine the filename

```
YYYY-MM-DD-<short-slug>.md
```
Example: `2026-05-09-use-smac-incumbent.md`

### 2. Fill the template

```markdown
# Decision: <title>

Date: YYYY-MM-DD
Status: proposed | accepted | superseded

## Context

What situation forced this decision? Reference the relevant experiment note
or reviewer comment ID if applicable.

## Decision

What did we choose? State it in one clear sentence.

## Rationale

Why is this the right choice now? Include trade-offs considered.

## Consequences

- Positive: what this enables or simplifies
- Negative: what this rules out or complicates
- Follow-up: tasks that must happen because of this decision
```

### 3. Cross-reference

- If the decision was triggered by an experiment, add a link from the experiment note.
- If it supersedes an older decision, mark the old file `Status: superseded` and
  add a `Superseded by: YYYY-MM-DD-<new-slug>.md` line.
- If it scopes out work, record in `decisions/` with
  `Status: accepted` and add to `next_steps.md`.

## Naming Examples

| Situation | Filename |
|-----------|----------|
| Choosing a solver config | `2026-05-09-use-smac-incumbent.md` |
| Deferring a task | `2026-05-24_deferred_items.md` |
| Changing narrative framing | `2026-05-24_narrative_pivot.md` |
| Answering an open question | `2026-05-25_open_questions.md` |

## Rules

- One decision per file — don't bundle multiple unrelated choices.
- Always state what was NOT chosen (the rejected alternatives).
- Keep records even for "obvious" choices — reviewers will ask.
