#!/usr/bin/env python3
"""Scripted, all-or-nothing edits for a manuscript revision pass.

    python3 revision_patch.py path/to/working_copy.tex

Fill in the EDITS section. Rules the helpers enforce:
  - sub(old, new): `old` must occur EXACTLY once, or the whole run aborts and
    the file is left untouched (nothing is written until every edit matched).
  - block(start, end, new): replaces whole lines from the one containing
    `start` (must match exactly one line) to the first line at or after it
    containing `end`. Use it for lines that carry long `% XX:` notes.
  - Write patterns as raw strings (r"...") so LaTeX backslashes survive. A raw
    string does not turn \\n into a newline: use block() for multi-line spans.
"""
import sys
from pathlib import Path

src = Path(sys.argv[1])
text = src.read_text()
applied = []


def sub(old, new, count=1):
    global text
    n = text.count(old)
    assert n == count, "expected %d match(es), found %d for: %r" % (count, n, old[:80])
    text = text.replace(old, new)
    applied.append(("sub", old[:50]))


def block(start, end, new):
    global text
    lines = text.split("\n")
    hits = [i for i, l in enumerate(lines) if start in l]
    assert len(hits) == 1, "start %r matched %d lines" % (start[:60], len(hits))
    i = hits[0]
    j = next(k for k in range(i, len(lines)) if end in lines[k])
    lines[i : j + 1] = new.split("\n") if new != "" else []
    text = "\n".join(lines)
    applied.append(("block", start[:50]))


# ----------------------------------------------------------------- EDITS
# Group them in this order: debris, numbers, repetition, terminology, then the
# rewritten Abstract/Summary/Conclusions. Example:
#
# sub(r"for the. melamine", r"for the melamine")
# block("% JK: this is a repetition", "% JK: this is a repetition", "")

# ------------------------------------------------------------------- END
src.write_text(text)
print("applied %d edits to %s" % (len(applied), src))
