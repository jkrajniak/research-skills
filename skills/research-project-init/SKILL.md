---
name: research-project-init
description: Bootstraps the standard four-repo research workspace (code / paper / private research notebook / large artifacts) used across ML/OR/computational-science projects. Use once a new research project has a one-page action brief with buy-in (see research-action-brief), or when an existing project's notes, code, and manuscript are tangled together in one repo and need separating.
allowed-tools: [Read, Write, Bash]
---

# Research Project Init

Bootstraps the standard research workspace used across ML/OR research projects.

## Workspace Layout

```
<workspace>/
  AGENTS.md                    ← AI context file (entry point for every agent)
  <proj>-code/                 ← public implementation (git, runnable)
  <proj>-paper/                ← manuscript (LaTeX, figures, tables)
  <proj>-research/             ← private lab notebook (plans, decisions, logs)
  <proj>-artifacts/            ← large generated files, outside git
```

## Steps

### 0. Write the action brief first

Before creating a single directory, write the one-page action brief (see
the `research-action-brief` skill): the question, the experiment, a staged
plan, and exactly what's needed from collaborators. Circulate it and get a
"go" before scaffolding anything below — the workspace and the proposal are
both an investment; the brief is how you find out whether that investment
is warranted while it's still cheap to redirect.

### 1. Create directories

```bash
PROJECT=my-algo
mkdir -p ${PROJECT}-code ${PROJECT}-paper ${PROJECT}-artifacts
mkdir -p ${PROJECT}-research/{experiments,decisions,notebook,templates,scripts,openspec/changes,paper/drafts}
```

### 2. Create AGENTS.md at workspace root

Required sections:
- `## Project Map` — one bullet per repo with its purpose and what belongs there
- `## Operating Rules` — tool choices (uv, git), promotion rules, reproducibility requirements
- `## Common Commands` — per-repo quick-reference
- `## Research Standards` — traceability rules for paper claims

### 3. Initialise the research notebook

Create `<proj>-research/README.md` with:
- Workflow (plan → experiments/ → decisions/ → notebook/)
- Boundaries (what goes where, what never gets committed)

Create `<proj>-research/artifacts_index.md` as a Markdown table:
`| Date | Artifact | Path | Code Commit | SHA256 | Notes |`

Create `<proj>-research/experiments/EVIDENCE_BASE.md` pinning which
artifact archives back each paper claim (fill in as experiments complete).

### 4. Add integrity check script

Copy `../scripts/check_evidence_integrity.sh` from this plugin into
`<proj>-research/scripts/`. It:
- Reads SHA-256 entries from EVIDENCE_BASE.md
- Runs `shasum -a 256 -c` against each pinned archive
- Exits non-zero on any mismatch

### 5. Copy templates

Copy `../templates/experiment_note.md`, `../templates/decision_record.md`,
and `../templates/action_brief.tex` from this plugin into
`<proj>-research/templates/`.

### 6. Init git repos (not artifacts/)

```bash
git -C ${PROJECT}-code    init
git -C ${PROJECT}-paper   init
git -C ${PROJECT}-research init
# artifacts dir is NOT a git repo — too large for version control
```

## Key Rules

- NEVER commit large archives to git — store in `<proj>-artifacts/`.
- ALWAYS record the code commit SHA in every experiment note.
- ALWAYS compute SHA-256 for every artifact archive.
- Keep AGENTS.md current — it is the agent's entry point.
- Promote code/configs only when stable; promote text/figures only when polished.
