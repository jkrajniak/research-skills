---
name: research-paper-audit
description: Audits a draft manuscript for repeated content, numbers that disagree between text, tables, and figures, terminology drift, overclaiming, and edit debris, using a lint script plus a semantic read. Use after each drafting or revision round and before submission or sending a draft to co-authors. Works on LaTeX; best with a numbers registry and claim ledger from research-paper-outline.
allowed-tools: [Read, Write, Edit, Bash, Grep]
---

# Research Paper Audit

Run after every drafting or revision round, and always before submission.
Local patches ("add a sentence about X") are how repetition and misaligned
numbers get in; this skill is the global re-check no patch triggers.

## When to use

- After a drafting or revision round, before circulating to co-authors
- Before submission or resubmission
- When the draft feels long, repetitive, or a reviewer says numbers disagree

## Steps

### 1. Run the mechanical lint

```bash
python3 ../scripts/check_paper_consistency.py main.tex \
    --numbers numbers.json --glossary glossary.json --claims claims.md
```

Without the registry files it still runs the debris, reference, duplicate,
and number-drift checks. It follows `\input`/`\include`. Exit code is 1 on
any ERROR (`--strict`: on WARN too). What it checks:

| Check | Catches |
|---|---|
| debris | `[?]`, `??`, `TODO`, sentences cut after a function word ("for the. melamine"), doubled words, revision-history language ("the version first submitted") |
| refs | undefined `\ref`/`\cite`, unused labels and bib entries |
| numbers | `\num{}` keys missing from the registry; the same quantity written with different values in different places; hand-typed copies of registry values; one number retyped in 3+ sections |
| duplicate | near-identical sentences in different sections |
| glossary | banned term variants; internal ids in prose |
| claims | ledger rows with no evidence, or pointing at labels that do not exist |

Fix every ERROR. Triage WARNs: each names `file:line`; a drifting pair is
either a real inconsistency or two different quantities that need two
registry keys and distinguishing words.

### 2. Do the semantic pass (the lint cannot)

Read the PDF or source with these questions, and record each finding as
`file:line` with the fix:

1. **Text vs. table.** For every sentence that summarises a table or figure
   ("differ by 0.7% to 1.5%", "nine decompositions", "within 0.015 degrees"),
   recompute the range, count, or bound from the table or the list in the
   text. Check each endpoint, not just the order of magnitude.
2. **Unit of counting.** "Seven systems", "five benchmarked systems", eight
   table rows: does each count say what it counts?
3. **Provenance of repeated values.** Where a number appears with several
   values (single run vs. mean, short vs. long production), is the reason
   stated at each place, or is it silently three different numbers?
4. **Precision vs. resolution.** Are differences quoted finer than the bin
   width, step size, or statistical error that limits them?
5. **Claims vs. evidence.** For each sentence in the Abstract and
   Conclusions, find its ledger row and its evidence. Flag:
   - superlatives that the Results contradict ("the one disagreement we
     found", "robust") when Results list several;
   - maxima replaced by convenient values ("up to 2500 K" when another
     system reaches 5950 K);
   - claims whose evidence is not in the paper (a parity check described in
     Methods with no result in Results).
6. **Same-time-point labelling.** Counts or percentages for the same
   quantity at different stages (after placement vs. after relaxation) must
   say which stage.
7. **Versions and identifiers.** Software version, DOI, commit hash, and
   reference entries must agree everywhere (text, Software availability,
   reference list, Program Summary).
8. **Placement.** Is Methods content sitting in Results, a Results sentence
   in Software availability, or protocol text repeated per system instead of
   once?

### 3. Cut repetition

For each fact told more than once, keep it at its **home** and replace the
rest:

- Same section family (Abstract/Summary/Conclusions): one sentence each,
  generated from headline rows, using `\num{}`.
- Protocol parameters: once in Methods or a protocol table, then
  `Section~\ref{}` or `the protocol of Section~\ref{}`.
- Limits: once under Limits; elsewhere a pointer.
- Journal summary fields (e.g. "Nature of problem", "Additional comments"):
  trim to what the field asks for; do not paste the abstract or methods.

Re-run the lint. A cut is not done until the audit is clean and the page
count went down or stayed level.

### 4. Write the audit note

Save `<proj>-paper/audit/YYYYMMDD_audit.md`: lint summary line, semantic
findings with `file:line`, what was fixed, what was deferred and why. Link
it from the next experiment note or decision record if a finding changed a
methodological choice (`research-decision-record`).

## Rules

- A clean lint run is necessary, not sufficient. Always do the semantic pass
  before submission.
- Fix the source (registry, ledger, glossary) first, then the prose. Never
  fix a number in the text only.
- If a number in the paper does not match its archive, the archive wins;
  re-derive from `research-artifact-archive`'s pinned output and update the
  registry.
- Do not silence a WARN by rewording to dodge the heuristic. Resolve the
  underlying inconsistency.
