# research-skills

Six [Claude Code](https://claude.com/claude-code) skills for running a computational research project reproducibly — the workspace layout, logging, and evidence-tracking habits that make a six-month-old result explainable again, instead of an archaeology project.

## Starting a new project

Write the brief before you write anything else:

1. **[`research-action-brief`](skills/research-action-brief)** — a one-page circulable brief: the question, the experiment, a staged plan, exactly what you need from collaborators. Get a "go" before investing further.
2. **[`research-project-init`](skills/research-project-init)** — once the brief has buy-in, bootstrap the code / paper / private-notebook / artifacts workspace split.
3. Then, as the project runs: `research-experiment-log`, `research-decision-record`, and `research-artifact-archive` keep every run, choice, and result traceable; `rigorous-debugging-discipline` covers the hard-to-localize-bug case.

## What's in here

| Skill | Use when |
|---|---|
| [`research-action-brief`](skills/research-action-brief) | Starting a new project, or an existing longer proposal needs a one-page version a collaborator will actually read |
| [`research-project-init`](skills/research-project-init) | The brief has buy-in — bootstraps the code / paper / private-notebook / artifacts split |
| [`research-experiment-log`](skills/research-experiment-log) | Before or after a non-trivial run — records the exact command, commit, and outputs |
| [`research-decision-record`](skills/research-decision-record) | A parameter, baseline, or methodology choice a reviewer might later question |
| [`research-artifact-archive`](skills/research-artifact-archive) | After a run whose outputs will back a paper claim — hash-and-timestamp before the next run overwrites it |
| [`rigorous-debugging-discipline`](skills/rigorous-debugging-discipline) | Chasing an intermittent or hard-to-localize bug in numerical/scientific code |

None of these are specific to one field — they came out of computational-physics and ML/OR work, but the underlying problem (a claim that can't be traced back to the run that produced it, or a project that never got off the ground because nobody would read the proposal) shows up anywhere code produces numbers that end up in a paper.

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

`templates/` and `scripts/` hold the plain files the skills generate from — an experiment-note template, a decision-record template, a one-page action-brief LaTeX skeleton, and the evidence-integrity check script. They're referenced by the skills but usable standalone.

## License

MIT — see [LICENSE](LICENSE).
