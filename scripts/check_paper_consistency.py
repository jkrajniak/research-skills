#!/usr/bin/env python3
"""Lint a LaTeX manuscript for the defects that survive many revision rounds:
numbers that drift, facts told in several sections, terminology drift,
edit debris, and unresolved references.

    python3 scripts/check_paper_consistency.py main.tex \
        [--numbers numbers.json] [--glossary glossary.json] \
        [--claims claims.md] [--strict] [--json]

Follows \\input / \\include. Stdlib only. Exit 1 on any ERROR (or on WARN
with --strict). Findings are heuristics: each one names file:line so a human
or Claude can judge it. A clean run means "no mechanical defects", not "the
paper is consistent"; the semantic pass in research-paper-audit covers the rest.

Severity:
  ERROR  certainly wrong (unresolved ref, [?], registry macro missing, debris)
  WARN   probably wrong (banned term, drifting number, duplicated sentence)
  INFO   worth a look (headline number repeated by hand, unused label)
"""
import argparse
import itertools
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------- loading

INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
SECTION_RE = re.compile(r"\\(section|subsection|subsubsection)\*?\{([^}]*)\}")
ABSTRACT_RE = re.compile(r"\\begin\{abstract\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:auto|c|C|eq|v)?ref\{([^}]+)\}")
CITE_RE = re.compile(r"\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]+)\}")
BIB_RE = re.compile(r"\\(?:bibliography|addbibresource)\{([^}]+)\}")
NUM_MACRO_RE = re.compile(r"\\num\{([^}]+)\}")


def strip_comment(line):
    out, i = [], 0
    while i < len(line):
        if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
            break
        out.append(line[i])
        i += 1
    return "".join(out)


def load_tex(path, seen=None):
    """Return a list of (file, lineno, text) with comments stripped and
    \\input files inlined."""
    seen = seen or set()
    path = Path(path)
    if path in seen or not path.exists():
        return []
    seen.add(path)
    rows = []
    for n, raw in enumerate(path.read_text(errors="replace").splitlines(), 1):
        line = strip_comment(raw)
        m = INPUT_RE.search(line)
        if m:
            sub = path.parent / m.group(1)
            if not sub.suffix:
                sub = sub.with_suffix(".tex")
            rows.extend(load_tex(sub, seen))
            continue
        rows.append((str(path), n, line))
    return rows


class Findings:
    def __init__(self):
        self.items = []

    def add(self, sev, check, where, msg):
        self.items.append(
            {"severity": sev, "check": check, "where": where, "message": msg}
        )


# ---------------------------------------------------------------- sections


def assign_sections(rows):
    """Annotate each row with a section id. Front matter before the first
    \\section is 'Abstract' if an abstract environment is seen, else 'Front'."""
    out, section = [], "Front"
    for f, n, t in rows:
        if ABSTRACT_RE.search(t):
            section = "Abstract"
        m = SECTION_RE.search(t)
        if m:
            section = m.group(2).strip() or section
        out.append((f, n, t, section))
    return out


# ---------------------------------------------------------------- checks

DEBRIS = [
    # (pattern, flags, severity, why)
    (r"\[\?\s*\]|\?\?", 0, "ERROR", "unresolved citation or reference marker"),
    (r"\b(?:TODO|FIXME|XXX|TBD)\b", 0, "ERROR", "leftover placeholder"),
    (r"\b(?:the|a|an|of|for|and|to|in|with|by|on)\.\s+[a-z]", 0, "ERROR",
     "sentence broken after a function word (edit debris)"),
    (r"\b(\w{2,})\s+\1\b", re.IGNORECASE, "WARN", "doubled word"),
    (r"first submitted|previous version of this (?:manuscript|article)|"
     r"in this revision|as requested by|the reviewers?\b|reviewer \d|"
     r"in response to|newly added", re.IGNORECASE, "WARN",
     "revision-history language (belongs in the response letter, not the paper)"),
]


def check_debris(rows, fnd):
    for f, n, t, _ in rows:
        for pat, flags, sev, why in DEBRIS:
            for m in re.finditer(pat, t, flags):
                ctx = t[max(0, m.start() - 20): m.end() + 20].strip()
                fnd.add(sev, "debris", "%s:%d" % (f, n), "%s: ...%s..." % (why, ctx))


def check_refs(rows, bib_dirs, fnd):
    labels, refs, cites = {}, defaultdict(list), defaultdict(list)
    bib_files = []
    for f, n, t, _ in rows:
        for m in LABEL_RE.finditer(t):
            labels[m.group(1)] = "%s:%d" % (f, n)
        for m in REF_RE.finditer(t):
            for key in m.group(1).split(","):
                refs[key.strip()].append("%s:%d" % (f, n))
        for m in CITE_RE.finditer(t):
            for key in m.group(1).split(","):
                cites[key.strip()].append("%s:%d" % (f, n))
        for m in BIB_RE.finditer(t):
            bib_files += [b.strip() for b in m.group(1).split(",")]
    for key, where in refs.items():
        if key not in labels:
            fnd.add("ERROR", "refs", where[0], "\\ref to undefined label '%s'" % key)
    for key, where in labels.items():
        if key not in refs and key.split(":")[0] in ("fig", "tab", "sec", "eq"):
            fnd.add("INFO", "refs", where, "label '%s' is never referenced" % key)
    bib_keys = set()
    for b in bib_files:
        p = Path(b)
        for cand in (p, p.with_suffix(".bib")):
            for base in bib_dirs:
                q = base / cand
                if q.exists():
                    bib_keys |= set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", q.read_text(errors="replace")))
    if bib_keys:
        for key, where in cites.items():
            if key not in bib_keys:
                fnd.add("ERROR", "refs", where[0], "\\cite key '%s' not in the .bib file" % key)
        for key in sorted(bib_keys - set(cites)):
            fnd.add("INFO", "refs", "bib", "bib entry '%s' is never cited" % key)
    return labels


NUM_TOKEN = re.compile(
    r"(?<![\w.])(\d[\d\s,]*(?:\.\d+)?(?:\s*(?:\\times|×|x)\s*10\^\{?-?\d+\}?)?)"
    r"(?:\s*(?:\\,|~|\\ )?\s*(?:\\?%|\\si\{[^}]*\}|[A-Za-zµ°][A-Za-z°/µ\-\^0-9]{0,8}))?"
)
UNIT_OK = re.compile(
    r"^(K|ps|ns|fs|us|ms|s|nm|Å|\\AA|%|\\%|atm|kcal|kJ|kT|g|rank|ranks|ps|min|h|GPa|MPa|bar|eV|Hz|GHz|x|×|°)$"
)
STOP = set(
    "the a an of for and to in with by on at is are was were be as from that this "
    "it its we our which than then also not no".split()
)


def numeric_value(raw):
    s = raw.replace(" ", "").replace(",", "")
    m = re.match(r"^(\d+(?:\.\d+)?)(?:(?:\\times|×|x)10\^\{?(-?\d+)\}?)?$", s)
    if not m:
        return None
    v = float(m.group(1))
    if m.group(2):
        v *= 10 ** int(m.group(2))
    return v


def extract_quantities(rows):
    """Yield (file, line, section, value, unit, context_words) for numbers that
    carry a unit; bare integers are too noisy to compare."""
    out = []
    for f, n, t, sec in rows:
        if t.lstrip().startswith("\\") and not t.lstrip().startswith(("\\item", "\\textbf")):
            continue
        plain = re.sub(r"\$|\\[a-zA-Z]+\*?(?:\{[^}]*\})?", " ", t) if False else t
        for m in NUM_TOKEN.finditer(plain):
            tail = plain[m.end(1): m.end()].strip(" ~\\,")
            unit = tail.replace("\\%", "%").replace("\\AA", "Å")
            val = numeric_value(m.group(1))
            if val is None or not unit or not UNIT_OK.match(unit):
                continue
            before = re.findall(r"[A-Za-z]{3,}", plain[max(0, m.start() - 60): m.start()].lower())
            after = re.findall(r"[A-Za-z]{3,}", plain[m.end(): m.end() + 40].lower())
            ctx = {w for w in before[-5:] + after[:3] if w not in STOP}
            out.append((f, n, sec, val, unit, ctx, m.group(0).strip()))
    return out


def check_numbers(rows, registry, fnd, repeat_sections):
    quantities = extract_quantities(rows)

    # 1. registry macros used but undefined / registry keys never used
    used = set()
    for f, n, t, _ in rows:
        for m in NUM_MACRO_RE.finditer(t):
            used.add(m.group(1))
            if registry is not None and m.group(1) not in registry:
                fnd.add("ERROR", "numbers", "%s:%d" % (f, n), "\\num{%s} is not in the registry" % m.group(1))
    if registry is not None:
        for key in sorted(k for k in registry if not k.startswith("_") and k not in used):
            fnd.add("INFO", "numbers", "registry", "'%s' is defined but never used in the text" % key)

    # 2. hand-typed value equal to / near a registry value with the same unit
    if registry:
        for key, e in registry.items():
            if key.startswith("_") or "value" not in e:
                continue
            unit = (e.get("unit") or "").replace("\\%", "%")
            for f, n, sec, val, u, ctx, raw in quantities:
                if u != unit or val == 0:
                    continue
                rel = abs(val - e["value"]) / abs(e["value"]) if e["value"] else 1
                if rel == 0:
                    fnd.add("INFO", "numbers", "%s:%d" % (f, n), "'%s' typed by hand; use \\num{%s}" % (raw, key))
                elif rel < 0.05 and (ctx & set(re.findall(r"[a-z]{3,}", key.lower()))):
                    fnd.add("WARN", "numbers", "%s:%d" % (f, n), "'%s' is within %.1f%% of registry '%s' (= %s); same quantity written differently?" % (raw, rel * 100, key, e["value"]))

    # 3. same quantity restated with a different value in different places
    by_unit = defaultdict(list)
    for q in quantities:
        by_unit[q[4]].append(q)
    seen_pairs = set()
    for unit, qs in by_unit.items():
        for a, b in itertools.combinations(qs, 2):
            if a[3] == b[3] or a[3] == 0 or b[3] == 0:
                continue
            rel = abs(a[3] - b[3]) / max(abs(a[3]), abs(b[3]))
            if rel < 0.05 and len(a[5] & b[5]) >= 2 and (a[0], a[1]) != (b[0], b[1]):
                key = (a[6], b[6], unit)
                if key in seen_pairs:
                    continue
                seen_pairs.add(key)
                fnd.add("WARN", "numbers", "%s:%d / %s:%d" % (a[0], a[1], b[0], b[1]),
                        "'%s' vs '%s' (%.1f%% apart, shared context: %s). Same quantity? Give both the same source." %
                        (a[6], b[6], rel * 100, ", ".join(sorted(a[5] & b[5]))))

    # 4. identical hand-typed quantity repeated in many sections
    spread = defaultdict(set)
    where = {}
    for f, n, sec, val, u, ctx, raw in quantities:
        spread[(val, u)].add(sec)
        where.setdefault((val, u), "%s:%d" % (f, n))
    for (val, u), secs in spread.items():
        if len(secs) >= repeat_sections:
            fnd.add("INFO", "numbers", where[(val, u)],
                    "%s %s appears by hand in %d sections (%s). Make it a registry value, or state it once and refer back." %
                    (val, u, len(secs), ", ".join(sorted(secs))))


def sentences(rows):
    """Split prose into sentences with provenance. Skips table/figure/code lines."""
    out, buf, start = [], [], None
    skip_env = 0
    for f, n, t, sec in rows:
        if re.search(r"\\begin\{(tabular|table|figure|equation|align|lstlisting|verbatim|thebibliography)", t):
            skip_env += 1
        if skip_env:
            if re.search(r"\\end\{(tabular|table|figure|equation|align|lstlisting|verbatim|thebibliography)", t):
                skip_env -= 1
            continue
        if t.strip().startswith("\\") and not t.strip().startswith(("\\item", "\\emph", "\\textbf")):
            if buf:  # a command line ends the paragraph (\section, \begin{...})
                out.append((" ".join(buf), pf, start, psec))
                buf = []
            continue
        if not t.strip():
            if buf:
                out.append((" ".join(buf), pf, start, psec))
                buf = []
            continue
        if not buf:
            start, pf, psec = n, f, sec
        buf.append(t.strip())
        if len(buf) > 40:
            out.append((" ".join(buf), pf, start, psec))
            buf = []
    if buf:
        out.append((" ".join(buf), pf, start, psec))
    sents = []
    for para, f, n, sec in out:
        para = re.sub(r"\\(?:cite|ref|eqref|label)[a-zA-Z]*\{[^}]*\}", "", para)
        para = re.sub(r"\\[a-zA-Z]+\*?\{([^}]*)\}", r"\1", para)
        para = re.sub(r"[\$\\{}~]", " ", para)
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", para):
            words = re.findall(r"[a-z0-9]+", s.lower())
            if len(words) >= 10:
                sents.append((s.strip(), words, f, n, sec))
    return sents


def check_duplicates(rows, fnd, threshold):
    sents = sentences(rows)
    sets = [set(w for w in words if w not in STOP) for _, words, *_ in sents]
    for i, j in itertools.combinations(range(len(sents)), 2):
        a, b = sents[i], sents[j]
        if a[4] == b[4]:  # same section: normal elaboration
            continue
        inter = len(sets[i] & sets[j])
        union = len(sets[i] | sets[j])
        if union and inter / union >= threshold and inter >= 6:
            fnd.add("WARN", "duplicate", "%s:%d (%s) / %s:%d (%s)" % (a[2], a[3], a[4], b[2], b[3], b[4]),
                    "near-duplicate sentences (%.0f%% overlap): \"%s...\" | \"%s...\"" %
                    (100 * inter / union, a[0][:70], b[0][:70]))


def check_glossary(rows, glossary, fnd):
    for entry in glossary.get("terms", []):
        canon = entry["canonical"]
        for banned in entry.get("banned", []):
            pat = re.compile(r"\b%s\b" % re.escape(banned), re.IGNORECASE)
            for f, n, t, _ in rows:
                if pat.search(t):
                    fnd.add("WARN", "glossary", "%s:%d" % (f, n), "'%s' used; canonical term is '%s'" % (banned, canon))
    for entry in glossary.get("internal_ids", []):
        pat = re.compile(r"\b%s\b" % re.escape(entry["id"]))
        for f, n, t, _ in rows:
            if pat.search(t):
                fnd.add("WARN", "glossary", "%s:%d" % (f, n), "internal id '%s' leaked into prose; write '%s'" % (entry["id"], entry.get("public", "its public name")))


def check_claims(path, labels, fnd):
    """claims.md ledger: | ID | Claim | Evidence | Home (label) | Headline |"""
    rows = [l for l in Path(path).read_text().splitlines() if l.strip().startswith("|")]
    for line in rows[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or re.fullmatch(r"-+", cells[0].replace(":", "")):
            continue
        cid, claim, evidence, home, headline = cells[:5]
        if cid.lower() in ("id", "") or cid.startswith("<"):
            continue
        if not evidence or evidence.startswith("<"):
            fnd.add("ERROR", "claims", "%s:%s" % (path, cid), "claim has no evidence: '%s'" % claim[:60])
        if home and not home.startswith("<") and home not in labels:
            fnd.add("ERROR", "claims", "%s:%s" % (path, cid), "home label '%s' does not exist in the manuscript" % home)
        for ev in re.findall(r"`?((?:tab|fig|eq):[\w:.-]+)`?", evidence):
            if ev not in labels:
                fnd.add("ERROR", "claims", "%s:%s" % (path, cid), "evidence label '%s' does not exist" % ev)


# ---------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tex")
    ap.add_argument("--numbers")
    ap.add_argument("--glossary")
    ap.add_argument("--claims")
    ap.add_argument("--dup-threshold", type=float, default=0.6)
    ap.add_argument("--repeat-sections", type=int, default=3)
    ap.add_argument("--strict", action="store_true", help="exit 1 on WARN too")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rows = assign_sections(load_tex(a.tex))
    if not rows:
        print("no input read from %s" % a.tex, file=sys.stderr)
        return 2
    fnd = Findings()
    registry = json.loads(Path(a.numbers).read_text()) if a.numbers else None
    base = Path(a.tex).parent

    check_debris(rows, fnd)
    labels = check_refs(rows, [base, Path(".")], fnd)
    check_numbers(rows, registry, fnd, a.repeat_sections)
    check_duplicates(rows, fnd, a.dup_threshold)
    if a.glossary:
        check_glossary(rows, json.loads(Path(a.glossary).read_text()), fnd)
    if a.claims:
        check_claims(a.claims, labels, fnd)

    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    fnd.items.sort(key=lambda x: (order[x["severity"]], x["check"], x["where"]))
    counts = {s: sum(1 for i in fnd.items if i["severity"] == s) for s in order}
    if a.json:
        print(json.dumps({"counts": counts, "findings": fnd.items}, indent=2))
    else:
        for i in fnd.items:
            print("%-5s [%s] %s\n      %s" % (i["severity"], i["check"], i["where"], i["message"]))
        print("\n%d ERROR, %d WARN, %d INFO" % (counts["ERROR"], counts["WARN"], counts["INFO"]))
    return 1 if counts["ERROR"] or (a.strict and counts["WARN"]) else 0


if __name__ == "__main__":
    sys.exit(main())
