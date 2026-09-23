---
name: research-action-brief
description: Lays out a one-page, circulable action brief — the standard way to start a new scientific research project, and also the short form of an existing longer proposal, built for a collaborator to skim in two minutes. Use when kicking off a new project and you want alignment and inputs before committing to workspace scaffolding or a full proposal, or when an existing longer proposal or plan needs a version other people will actually read.
allowed-tools: [Read, Write, Bash]
---

# Research Action Brief

Produces a one-page (occasionally two) circulable brief. This is the
**default first artifact of a new research project** — write it before the
full proposal, before the workspace exists, before any code. It is cheap to
write, cheap to revise, and it gets a collaborator's input or sign-off in the
time it takes to read one page, instead of after they've read (or skipped)
a ten-page document.

It also works the other way round, as the short form of a proposal that
already exists. Either way the brief is not a summary — it exists to get a
specific decision or specific inputs from a specific reader, fast.

## When to use

- **Starting a new research project.** Write the brief first: the question,
  the experiment, a staged plan, and exactly what you need from
  collaborators — before running `research-project-init` to scaffold the
  four-repo workspace, and before the full proposal document exists. The
  brief is what you circulate to get a "yes, go ahead" or "here's what's
  missing" before investing in either.
- A longer proposal (`proposal.md` / a grant draft / a design doc) already
  exists, but nobody besides its author has read it end to end — distill it
  into a brief instead of asking people to read the whole thing.
- You need a concrete list of inputs from a collaborator before work can
  start (data, a judgment call, sign-off on a stage plan)
- A plan has stages whose dependencies matter more than a calendar, and
  that ordering needs to be visible at a glance

## Principles

- **It comes first, not last.** For a new project, the brief is written
  before the long proposal, before the workspace, before any code — it is
  the cheapest way to find out whether the idea survives contact with a
  collaborator's first question. Only write the long document once the
  brief has gotten a "go."
- **When a long document does exist, the brief is its twin, not a
  summary.** The brief and the long document should say the same thing; the
  brief just omits statistical detail, full prior-art discussion, and
  anything that isn't needed to make the decision at hand. Keep those in the
  long document and say so explicitly, so the reader knows where to look for
  more.
- **No calendar.** Order stages by dependency, not by date. Calendar
  planning is a separate conversation that happens after the team agrees
  on the sequence — putting dates in the brief invites the wrong argument.
- **Every stage answers three questions.** What question does this stage
  settle? What does it hand to the next stage? What condition would end
  the project here? A stage description that skips the third question
  reads as a task list, not a plan.
- **State what you are explicitly not doing.** A short "dropped" section,
  with the one-line reason for each drop, heads off most of the follow-up
  questions before they're asked.
- **The ask list is only things the reader can uniquely give you.**
  Building, running, and analysis belong on your side of the line; the
  brief's input list should be data, sign-off, or judgment calls only the
  reader has.
- **Either answer is a result.** If the brief is proposing an experiment,
  say plainly that a negative result is still the paper / still useful —
  otherwise the ask reads as fishing for a predetermined outcome.

## Steps

### 1. Draft the content first, in Markdown

Write the `.md` twin before touching layout: TL;DR, the question (stated
fairly enough that any answer would be a real result), the experiment or
plan, the staged breakdown, what's dropped, decisions/gates, and the ask
list. Get this reviewed before investing in the PDF layout — the content
structure is what makes the brief legible, not the typesetting.

### 2. Lay out the one-sheet PDF

Use `../templates/action_brief.tex` as the starting skeleton (a plain
single-file `pdflatex` article: `tcolorbox` for the masthead and callout
boxes, `tikz` for a stage-flow diagram and per-stage cards, a
colour-blind-safe accent palette, small badges for go/stop/blocking
status). Replace the placeholder network-sketch macro with whatever
schematic fits your domain, or delete it.

Compile and check it stays to the intended page count:

```bash
pdflatex -interaction=nonstopmode action_brief.tex
```

### 3. Circulate both forms

Send the `.md` where plain text is easier to reply inline to (email,
chat), and the `.pdf` where the visual layout carries meaning (a printed
copy, a slide-adjacent share). Keep both in sync — edit the Markdown
first, then port structural changes into the `.tex`.

## Rules

- Keep the brief itself free of anything that isn't needed for the
  decision at hand — full statistical design, complete prior-art
  discussion, and the risk register stay in the long document, referenced
  by name.
- Never let the ask list include something you could get yourself; if you
  can build, run, or look it up without the reader, don't ask them.
- A stage card without an end condition is incomplete — write "can end
  the project if" even when the honest answer is "unlikely."
- Update the brief when the plan changes. A brief a collaborator was
  asked to sign off on, and which then diverges silently from the real
  plan, is worse than not having one.
