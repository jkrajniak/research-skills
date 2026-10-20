# Claim ledger

One row per claim the paper makes. A claim lives in exactly one **home** section
(a `\label`); every other mention is a pointer or a one-line recap that reuses
the registry values. **Headline = yes** means it may appear in the Abstract,
Summary, and Conclusions. Nothing may appear there that is not headline here.

| ID | Claim (one sentence, with its number as `\num{key}`) | Evidence (`tab:`/`fig:` label or archive) | Home (label) | Headline |
|----|------|------|------|------|
| C1 | The port is validated on `\num{paper.n_systems}` systems. | `tab:validation` | `sec:validation` | yes |
| C2 | <claim> | <`tab:`/`fig:` label, or archive sha256> | <`sec:...`> | no |

## Limits and negative results

Same rules: one home each. List every disagreement with the reference here, so
the Conclusions can say "N disagreements" without miscounting.

| ID | Limit or disagreement | Evidence | Home (label) | Cause found? |
|----|------|------|------|------|
| L1 | <what does not match> | <label> | <`sec:...`> | yes / no / partly |
