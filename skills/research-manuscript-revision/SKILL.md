---
name: research-manuscript-revision
description: Runs a safe revision pass on an existing manuscript that has inline author or reviewer notes and consistency problems, by triaging every note, applying edits as an all-or-nothing script on a working copy, verifying with a compile and the audit lint, and delivering a change log that separates what was fixed from what only the author can answer. Use when a draft is full of "% XX:" comments, repetition, or misaligned numbers and you are asked to clean it up, or after research-paper-audit has produced findings to apply.
allowed-tools: [Read, Write, Edit, Bash, Grep]
---

# Research Manuscript Revision

Applies the findings of `research-paper-audit` and the author's own inline
notes to a manuscript, without inventing facts and without leaving the draft in
a half-edited state. Detection is `research-paper-audit`; planning is
`research-paper-outline`; this skill is the careful editing pass between them.

## When to use

- A draft carries many inline notes (`% JK: repetition`, `% what does this mean?`)
- The audit lint reports errors and warnings that need fixing in the source
- You are asked to "clean up", "tighten", or "make consistent" a paper

## Principles

- **Work on a copy, outside the repo.** Keep the original beside it for the
  diff. Do not publish or push the paper unless asked; a paper is not a
  skills-repo artifact.
- **Never invent a fact, number, or reference.** If the source does not
  support a fix, leave a `% TODO(author): <question>` and list it in the
  change log. References written from memory are flagged as unverified.
- **One home per fact.** When removing a repeat, keep it where the claim is
  argued, and point to it from the other places.
- **Edits are all-or-nothing.** A scripted patch whose every replacement must
  match exactly once cannot silently skip a change or half-apply.
- **Report faithfully.** If the paper did not get shorter, or a check could
  not be run, say so in the change log.

## Steps

### 1. Baseline

```bash
mkdir -p work && cp main.tex bibliography.bib work/ && cp main.tex work/main.orig.tex
python3 ../scripts/check_paper_consistency.py work/main.tex > work/audit_before.txt
```

Read the whole source once (not just the lint output). Compile the original
and keep its warnings as the baseline; stub figures if the image files are
missing (`\PassOptionsToPackage{draft}{graphicx}` before `\input{main.tex}`).
Install a minimal TeX set if none is present (`texlive-latex-base`,
`-latex-extra`, `-publishers`, `-fonts-recommended`).

### 2. Triage every note and finding

List each inline note and each lint finding, then assign exactly one outcome:

| Outcome | When | Action |
|---|---|---|
| Resolve from the text | The answer is in the paper (a definition, a pointer, a reason stated elsewhere) | Rewrite, delete the note |
| Remove | The note says "repetition, we said this before" and the earlier place exists | Cut the repeat, keep the home |
| Rewrite | The note says "unclear", "long sentence", "what does this mean?" | Split, enumerate, or define; delete the note |
| Needs the author | A fact, a decision, a missing result, a feature or code question, a citation you cannot verify | Leave the note, as `% TODO(author):` if it is yours |
| Correct a number | Text disagrees with its table or list | Recompute from the table; fix the text; flag the basis |

Fix the order of work: mechanical debris, then numbers and counts, then
repetition, then terminology, then the Abstract, Summary, and Conclusions
rewritten from the headline claims (`research-paper-outline`'s ledger).

### 3. Write the patch script

Copy `../templates/revision_patch.py` to the working directory and fill in
EDITS with `sub()` and `block()` calls. Run it on the working copy.

- Match on the **smallest unique snippet**; for lines carrying long notes use
  `block(start, end, new)`.
- Patterns are raw strings; `\n` in a raw string is not a newline, so use
  `block()` for multi-line spans.
- If an assertion fails, fix the pattern; never loosen it to "replace all".

### 4. Rebuild generated files and compile

If the paper uses a numbers registry, rebuild it (`build_numbers_tex.py`),
then compile: `pdflatex`, `bibtex`, `pdflatex` twice. Required result: no
undefined references or citations, no `[?]` in the PDF text
(`pdftotext main.pdf - | grep -c '\?\?'`), and no new errors against the
baseline.

### 5. Re-audit and measure

```bash
python3 ../scripts/check_paper_consistency.py main.tex \
    --numbers numbers.json --glossary glossary.json --claims claims.md
```

Triage each remaining WARN as real or false positive and say which. Count
words before and after. Lint false positives you hit (labels read as prose,
generated includes, notes in `.bib`) are bugs in the lint: fix the script.

### 6. Review your own diff adversarially

`diff -u main.orig.tex main.tex`. For every changed sentence ask: did I add a
claim the source does not support? Did I change a number's meaning (rounded vs
exact, single run vs mean)? Did the cut remove the only mention of something?
Revert or add a TODO where the answer is yes.

### 7. Deliver

Use `../templates/revision_changelog.md`. Its two closing sections are the
point: **Needs the author** (questions only they can answer) and **Please
verify** (anything from memory or inferred, and anything outside the source,
such as figure legends). Send the edited source, bibliography, registry files,
the diff, and the change log. Do not push the paper anywhere unless asked.

## Rules

- Never delete an author note you did not resolve.
- Never cite from memory without flagging it; prefer a TODO to a guessed
  reference.
- When two numbers conflict, choose the one the table or list supports, state
  the basis, and flag it for a recheck against the unrounded data.
- A count in the text that disagrees with an explicit list is a finding even
  if you cannot tell which one is wrong; pick one, flag it.
- Do not edit figure files or claim to have fixed text inside them.
- If the cleanup did not reduce length, say so; do not describe a rewrite as a
  cut.
