---
name: research-paper-outline
description: Plans a manuscript before drafting by building a claim ledger (each claim, its evidence, its one home section), a numbers registry, and a glossary, so every fact is stated once and every number comes from one source. Use before writing or restructuring a paper, when turning experiment notes into a draft, or when a draft has grown repetitive and its numbers no longer agree. Write the Abstract, Summary, and Conclusions last, from the ledger.
allowed-tools: [Read, Write, Bash]
---

# Research Paper Outline

Repetition and number drift in a paper come from the same cause: facts are
retyped by hand in several sections, and each revision patches one place.
This skill fixes it at the source. Decide **where each fact lives**, **where
each number comes from**, and **what each term is called** before any prose
exists. Then `research-paper-audit` can check the draft mechanically.

## When to use

- Before drafting a paper, or before restructuring one
- When turning `experiments/` notes and `EVIDENCE_BASE.md` into a manuscript
- When a draft says the same thing in the Abstract, Introduction, Results,
  and Conclusions, or its tables and text disagree

## Steps

### 1. Build the claim ledger

Copy `../templates/paper_claims.md` to `<proj>-paper/claims.md`. Seed it from
the action brief (`research-action-brief`): the question and each stage's
result become the first claims. One row per claim:

- **Claim**: one sentence. Put numbers in as `\num{key}`, not digits.
- **Evidence**: a table or figure label, or an archive pinned in
  `EVIDENCE_BASE.md`. No evidence, no claim.
- **Home**: the single section (`\label`) where it is argued in full.
- **Headline**: yes only if a reader who stops at the Abstract must know it.

List **limits and disagreements** in the second table, with whether a cause
was found. The Conclusions must be able to say how many there are.

### 2. Build the numbers registry

Copy `../templates/paper_numbers.json` to `<proj>-paper/numbers.json`. Add one
entry for every number a claim uses: value, format, unit, `source` (the
experiment note), and the archive `sha256`. When two runs give two values for
the "same" quantity (single run vs. seed mean), give them **two keys** and
say in `note` which one the text uses and why.

Generate the macros and include them in the preamble:

```bash
python3 ../scripts/build_numbers_tex.py numbers.json numbers.tex
```

```latex
\input{numbers.tex}      % in the preamble
... peaks at \num{dodecane.peak_T} ...
```

Rule: a number that appears in more than one place, or in the
Abstract/Summary/Conclusions, **must** be a `\num{}`. One-off values inside a
single table may stay literal.

### 3. Fix the vocabulary

Copy `../templates/paper_glossary.json` to `<proj>-paper/glossary.json`.

- **One name per concept**; list the variants you have already caught
  yourself using as `banned`.
- **Define each segmentation once** (stages, phases, tiers, validation
  levels) under `structure`, with a fixed count and fixed names. Parallel
  schemes for the same workflow ("three phases" here, "three stages" there,
  "four panels" in the figure) are the most common source of confusion.
- **List internal ids** (project codenames, file names) that must not reach
  the prose, with their public names.
- Fix the **unit of counting** for headline counts (systems vs. models vs.
  table rows) and record it in the registry `note`.

### 4. Allocate sections: one home per fact

Draft the section list from the ledger, not from the order the work was done.

| Section | Holds | Does not hold |
|---|---|---|
| Methods | Every protocol parameter, **once** (or a table of them) | Results, justification repeated per system |
| Results | The evidence for each claim, at its home | Protocol restatements; method detail |
| Limits | Each limit, once | Retellings spread across Methods and Conclusions |
| Abstract / Summary / Conclusions | Headline claims only, one sentence each, with `\num{}` values | Anything not marked headline; new numbers; new caveats |

Where a fact is needed elsewhere: **refer, don't retell** (`as in
Section~\ref{sec:protocol}`), or give a one-line recap with `\num{}` values.
Protocols that differ per system belong in one table in Methods, with a
column per difference, not in prose per system.

### 5. Order of writing

1. Methods and protocol table
2. Results sections, each opening with its claim ID in a `% claim: C3` comment
3. Limits
4. **Last**: Abstract, Program/Software Summary, Introduction's contribution
   paragraph, Conclusions, written from the headline rows only

Then run `research-paper-audit`.

## Rules

- No prose before the ledger exists. A section with no ledger row is either
  background or surplus; cut it or add the claim.
- Never retype a registry number. If the value changes, change the registry
  and rebuild.
- The Conclusions add no new fact. If a sentence there has no headline row,
  it is a Results sentence or it is cut.
- A negative or partial result gets a ledger row like any other. Counting
  limits honestly is what keeps "the one disagreement we found" from
  appearing next to four.
- Journal-mandated summaries (a software "Program Summary", a graphical
  abstract) are a third copy of the abstract by default. Fill them from the
  headline rows and keep each field to what that template asks for.
