#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lookup.py - build a compact terminology brief for a source text.

Scans a source text against the bundled term banks and emits ONLY the entries that
actually occur - the "terminology brief" the skill injects into the draft phase. This
keeps context lean: the full idiom/glossary banks (potentially thousands of rows) live
in TSV files and never enter model context; only the handful of relevant pairs do.

USAGE
    python lookup.py source.txt                 # EN source -> EN/FA brief
    python lookup.py --reverse source_fa.txt    # FA source -> match Persian column
    cat source.txt | python lookup.py
    python lookup.py --json source.txt

TSV format (scripts/data/*.tsv):  EN <TAB> FA <TAB> note(optional). '#' lines are comments.
"""
import argparse
import json
import os
import re
import sys

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
BANKS = [("idioms", "idioms.tsv"), ("glossary", "glossary.tsv")]
TITLES = {"idioms": "IDIOMS", "glossary": "GLOSSARY / COLLOCATIONS"}


def load(fname):
    path = os.path.join(DATA, fname)
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.lstrip().startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            en, fa = parts[0].strip(), parts[1].strip()
            note = parts[2].strip() if len(parts) > 2 else ""
            if en and fa:
                rows.append((en, fa, note))
    return rows


# light inflection tolerance (plural / 3sg / past / gerund)
_LEMMA_SUFFIX = r"(?:es|s|ed|ing|d)?"


def en_pattern(phrase):
    words = re.split(r"\s+", phrase.strip())
    escaped = [re.escape(w) for w in words]
    # Inflect the FINAL token so multi-word entries still match real text:
    # "business partner" -> "business partners", "lose your temper" -> "...tempered".
    # Applying it only to the last word keeps the match anchored and avoids false hits.
    escaped[-1] += _LEMMA_SUFFIX
    return re.compile(r"\b" + r"\s+".join(escaped) + r"\b", re.IGNORECASE)


def find_en(rows, text):
    t = re.sub(r"\s+", " ", text)
    return [(en, fa, note) for en, fa, note in rows if en_pattern(en).search(t)]


def find_fa(rows, text):
    return [(en, fa, note) for en, fa, note in rows if fa and fa.split("/")[0] in text]


def dedup(hits):
    seen, out = set(), []
    for h in hits:
        if h[0] not in seen:
            seen.add(h[0])
            out.append(h)
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description="Build a terminology brief for a source text.")
    p.add_argument("--reverse", action="store_true", help="FA source -> match Persian column")
    p.add_argument("--json", action="store_true")
    p.add_argument("file", nargs="?", default="-")
    a = p.parse_args(argv)
    text = open(a.file, encoding="utf-8").read() if a.file != "-" else sys.stdin.read()

    result = {}
    for label, fname in BANKS:
        rows = load(fname)
        hits = find_fa(rows, text) if a.reverse else find_en(rows, text)
        result[label] = dedup(hits)

    if a.json:
        print(json.dumps(
            {k: [{"en": e, "fa": f, "note": n} for e, f, n in v] for k, v in result.items()},
            ensure_ascii=False, indent=2))
        return 0

    total = sum(len(v) for v in result.values())
    if not total:
        print("(no idiom / glossary terms found in source)")
        return 0
    out = ["# Terminology brief (%d entr%s)\n" % (total, "y" if total == 1 else "ies")]
    for label, _ in BANKS:
        v = result[label]
        if not v:
            continue
        out.append("## " + TITLES[label])
        for e, f, n in v:
            out.append("- %s  ->  %s%s" % (e, f, ("   (" + n + ")" if n else "")))
        out.append("")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
