# research-skills

Eight [Claude Code](https://claude.com/claude-code) skills for running a computational research project reproducibly: the workspace layout, logging, and evidence-tracking habits that make a six-month-old result explainable again, and the paper-writing habits that keep the manuscript consistent with that evidence (one home per fact, one source per number).

## Starting a new project

Write the brief before you write anything else:

1. **[`research-action-brief`](skills/research-action-brief)**: a one-page circulable brief: the question, the experiment, a staged plan, exactly what you need from collaborators. Get a "go" before investing further.
2. **[`research-project-init`](skills/research-project-init)**: once the brief has buy-in, bootstrap the code / paper / private-notebook / artifacts workspace split.
3. Then, as the project runs: `research-experiment-log`, `research-decision-record`, and `research-artifact-archive` keep every run, choice, and result traceable; `rigorous-debugging-discipline` covers the hard-to-localize-bug case.

## Writing the paper

Repetition and numbers that disagree between text and tables come from retyping facts by hand and patching one section at a time. Two skills prevent that:

1. **[`research-paper-outline`](skills/research-paper-outline)**: before drafting, build a claim ledger (each claim, its evidence, its one home section), a numbers registry, and a glossary. Abstract and Conclusions are written last, from the ledger.
2. **[`research-paper-audit`](skills/research-paper-audit)**: after every draft or revision round, run the lint script and a semantic pass for drifting numbers, duplicated content, terminology drift, overclaiming, and edit debris.

## What's in here

| Skill | Use when |
|---|---|
| [`research-action-brief`](skills/research-action-brief) | Starting a new project, or an existing longer proposal needs a one-page version a collaborator will actually read |
| [`research-project-init`](skills/research-project-init) | The brief has buy-in. Bootstraps the code / paper / private-notebook / artifacts split |
| [`research-experiment-log`](skills/research-experiment-log) | Before or after a non-trivial run. Records the exact command, commit, and outputs |
| [`research-decision-record`](skills/research-decision-record) | A parameter, baseline, or methodology choice a reviewer might later question |
| [`research-artifact-archive`](skills/research-artifact-archive) | After a run whose outputs will back a paper claim. Hash-and-timestamp before the next run overwrites it |
| [`rigorous-debugging-discipline`](skills/rigorous-debugging-discipline) | Chasing an intermittent or hard-to-localize bug in numerical/scientific code |
| [`research-paper-outline`](skills/research-paper-outline) | Before drafting or restructuring a paper. Claim ledger, numbers registry, glossary, one home per fact |
| [`research-paper-audit`](skills/research-paper-audit) | After each draft or revision round, and before submission. Finds repetition, number drift, overclaims, debris |

None of these are specific to one field. They came out of computational-physics and ML/OR work, but the underlying problem (a claim that can't be traced back to the run that produced it, or a project that never got off the ground because nobody would read the proposal) shows up anywhere code produces numbers that end up in a paper.

## Install

As a Claude Code plugin marketplace:

```
/plugin marketplace add jkrajniak/research-skills
/plugin install research-skills
```

Or clone the skills you want directly into a project's `.claude/skills/` (or `~/.claude/skills/` for every project):

```bash
git clone https://github.com/jkrajniak/research-skills
cp -r research-skills/skills/research-experiment-log ~/.claude/skills/
```

## Templates and scripts

`templates/` and `scripts/` hold the plain files the skills generate from: experiment-note and decision-record templates, a one-page action-brief LaTeX skeleton, the paper claim-ledger / numbers-registry / glossary templates, the evidence-integrity check script, `build_numbers_tex.py` (registry to `\num{key}` LaTeX macros), and `check_paper_consistency.py` (manuscript lint, LaTeX, stdlib only). They're referenced by the skills but usable standalone.

```bash
python3 scripts/build_numbers_tex.py paper/numbers.json paper/numbers.tex
python3 scripts/check_paper_consistency.py paper/main.tex \
    --numbers paper/numbers.json --glossary paper/glossary.json --claims paper/claims.md
```

## License

MIT. See [LICENSE](LICENSE).
