---
name: research-artifact-archive
description: Packages a run's outputs into a tamper-evident, reproducible, timestamped archive with a SHA-256 checksum, and registers it in the artifact index. Use after any benchmark/experiment run whose outputs will back a paper claim, or when a run completes and results must be preserved before the next run overwrites them.
allowed-tools: [Read, Write, Bash]
---

# Research Artifact Archive

Packages a run's outputs into a tamper-evident, reproducible archive.

## When to use

- After any benchmark/experiment run whose outputs will back a paper claim
- When a run completes and results must be preserved before the next run overwrites them
- When creating a "pinned" evidence snapshot for manuscript submission

## Steps

### 1. Collect outputs

Gather all result files into a staging directory or confirm they are
already in a results subdirectory under `<proj>-code/`.

### 2. Create a timestamped archive

```bash
TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
ARCHIVE_NAME="<experiment_slug>_${TIMESTAMP}.tar.gz"
ARTIFACTS_DIR="../<proj>-artifacts/<category>"

mkdir -p "${ARTIFACTS_DIR}"
tar -czf "${ARTIFACTS_DIR}/${ARCHIVE_NAME}" \
    results/<relevant_subdir>/ \
    configs/<config_used>.json \
    scripts/<run_script>.py
```

### 3. Compute and store SHA-256

```bash
shasum -a 256 "${ARTIFACTS_DIR}/${ARCHIVE_NAME}" \
    | tee "${ARTIFACTS_DIR}/${ARCHIVE_NAME}.sha256"
```

### 4. Register in artifacts_index.md

Append to `<proj>-research/artifacts_index.md`:

```markdown
| YYYY-MM-DD | <short description> | `<relative path from workspace>` | `<git commit SHA>` | `<sha256 hash>` | <notes: what's inside, what it supersedes> |
```

### 5. (Optional) Pin in EVIDENCE_BASE.md

If this archive will be the source for paper numbers:

```markdown
| <role, e.g. "Final benchmark archive"> | `<path>` | `<sha256>` | ✓ YYYY-MM-DD |
```

Mark older superseded entries with `(superseded)` and move them to
the "Superseded" section of EVIDENCE_BASE.md.

### 6. Verify integrity

```bash
cd <proj>-research
bash scripts/check_evidence_integrity.sh ..
```

## Archive naming convention

```
<experiment_slug>_<YYYYMMDDTHHMMSSZ>[_<variant_tag>].tar.gz
```

Examples:
- `final_experiments_20260524T202545Z_partition_refreshed_v2.tar.gz`
- `smac_full_20260508T192425Z.tar.gz`

## What to include in the archive

| Include | Exclude |
|---------|---------|
| Result CSVs | Virtual environments |
| Config JSON used for the run | Raw solver log files (unless small) |
| The run script (snapshot) | Instance archives (reference separately) |
| Summary JSON / LaTeX tables | Intermediate checkpoint files |

## Rules

- One archive = one experiment run. Never overwrite — always create a new timestamped archive.
- SHA-256 file must be stored next to the archive (same directory).
- The archive content must be sufficient to reproduce any derived table or figure.
- Superseded archives are kept for audit; mark them clearly in EVIDENCE_BASE.md.
