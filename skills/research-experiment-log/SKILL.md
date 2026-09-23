---
name: research-experiment-log
description: Creates a dated experiment note before and after a non-trivial run, recording the exact command, code commit, outputs, and interpretation. Use before starting a non-trivial run, after a run completes, or when a run is blocked and the reason needs to be on record.
allowed-tools: [Read, Write, Bash]
---

# Research Experiment Log

Creates a dated experiment note in `<proj>-research/experiments/`.

## When to use

- Before starting a non-trivial run (fill Inputs section, Status=planned)
- After a run completes (fill Outputs + Observations + Interpretation)
- When a run is blocked (record what failed and why)

## Steps

### 1. Determine the filename

```
YYYYMMDD_<short_slug>.md
```
Example: `20260508_smac_calibration.md`

### 2. Fill the template

```markdown
# Experiment: <name>

Date: YYYY-MM-DD
Status: planned | running | completed | blocked

## Question
What specific question does this run answer?

## Inputs
- Code repo: `../<proj>-code/`
- Code commit: `<git short SHA>`
- Config: `<path to config file>`
- Command: `uv run python scripts/run_X.py --flag value`
- Instance set / data: `<path or archive name>`

## Outputs
- Result path: `../<proj>-artifacts/<archive_name>.tar.gz`
- Artifact archive: `<archive_name>.tar.gz`
- SHA256: `<hash>`

## Observations
- Key numbers (accuracy, gap, runtime, etc.)
- Any anomalies or surprises

## Interpretation
- What does this mean for the paper claim?
- Does it confirm or contradict the hypothesis?

## Next Steps
- Follow-up experiments needed
- Decisions to record in decisions/
```

### 3. Compute and record SHA-256

```bash
shasum -a 256 ../<proj>-artifacts/<archive>.tar.gz | tee ../<proj>-artifacts/<archive>.tar.gz.sha256
```

### 4. Add to artifacts_index.md

Append a row to `<proj>-research/artifacts_index.md`:

```
| YYYY-MM-DD | <description> | `../<proj>-artifacts/<archive>.tar.gz` | `<commit>` | `<sha256>` | <notes> |
```

### 5. Update EVIDENCE_BASE.md if this is paper-facing

If the outputs will back a paper claim, add or update an entry in
`<proj>-research/experiments/EVIDENCE_BASE.md`.

## Rules

- Record the exact command — it must be reproducible by someone else.
- Never leave the Code Commit field blank.
- SHA-256 is mandatory for every artifact that will back a paper claim.
- Keep observations factual; move interpretation to the Interpretation section.
