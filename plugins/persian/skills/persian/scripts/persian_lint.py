#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""persian_lint.py - deterministic Persian text mechanics normalizer / linter.

Pillar B of the `persian-pro` skill. Fixes the "small things" that make Persian
text look wrong no matter how good the word choice is: Arabic-vs-Persian letters,
digits, ZWNJ (نیم‌فاصله), punctuation, spacing, and kashida. None of this needs
human judgment, so it lives in code: repeatable, testable, fast.

USAGE
    python persian_lint.py --check  file.txt        # report issues only (default)
    python persian_lint.py --fix    file.txt        # print fixed text to stdout
    python persian_lint.py --fix --in-place file.txt
    cat file.txt | python persian_lint.py --fix     # stdin -> stdout
    python persian_lint.py --check --json file.txt  # machine-readable report

DIGIT POLICY (default = "persian")
    Convert Latin (0-9) and Arabic-Indic (٠-٩) digits to Persian (۰-۹) in prose,
    but NEVER inside code spans (``` ``` and `inline`), URLs, emails, or version
    numbers (v1.2.3, 2.4.1). A token that also has Latin letters (MP3, COVID-19,
    iPhone15) keeps Latin digits. Override with --digits {persian,latin,keep}.
    NOTE: unit conversion (feet->meters, F->C) is a *translation* decision, not a
    mechanics one - it is handled in the skill workflow (ask the user), never here.

DESIGN
    Safe by default. High-confidence fixes are applied; ambiguous cases (a bare
    «تر» that might mean "wet"; a glued «میرود») are reported, never auto-changed.
    Stdlib only.
"""
import argparse
import json
import re
import sys

ZWNJ = "‌"      # نیم‌فاصله / zero-width non-joiner
KASHIDA = "ـ"   # tatweel

CHAR_MAP = {
    "ي": "ی",  # ARABIC YEH    -> PERSIAN YEH
    "ى": "ی",  # ALEF MAKSURA  -> PERSIAN YEH
    "ك": "ک",  # ARABIC KAF    -> PERSIAN KEHEH
    "ة": "ه",  # TEH MARBUTA   -> HEH
}

LATIN_TO_FA = {ord(a): b for a, b in zip("0123456789", "۰۱۲۳۴۵۶۷۸۹")}
ARABIC_TO_FA = {ord(a): b for a, b in zip("٠١٢٣٤٥٦٧٨٩", "۰۱۲۳۴۵۶۷۸۹")}
FA_TO_LATIN = {ord(b): a for a, b in zip("0123456789", "۰۱۲۳۴۵۶۷۸۹")}
ARABIC_TO_LATIN = {ord(a): b for a, b in zip("٠١٢٣٤٥٦٧٨٩", "0123456789")}

# Convert digits only when the WHOLE alnum token is digits -> MP3, COVID-19 keep Latin.
_ALNUM_TOKEN = re.compile(r"[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*")

# ZWNJ plural/clitic suffixes, LONGEST-FIRST so alternation prefers them.
HA_SUFFIXES = ["هایشان", "هایتان", "هایمان", "هایی", "هایم", "هایت", "هایش", "های", "ها"]

# Never touch: fenced code, inline code, URLs, emails, version numbers.
_PROTECT = re.compile(
    r"```.*?```"
    r"|`[^`]*`"
    r"|(?:https?://|www\.)\S+"
    r"|[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"
    r"|\bv\d+(?:\.\d+)+\b"
    r"|\b\d+\.\d+\.\d+\b",
    re.DOTALL,
)
_SENTINEL = "\x00"


def _mask(text):
    spans = []

    def repl(m):
        spans.append(m.group(0))
        return _SENTINEL

    return _PROTECT.sub(repl, text), spans


def _unmask(text, spans):
    parts = text.split(_SENTINEL)
    out = parts[0]
    for i, part in enumerate(parts[1:]):
        out += (spans[i] if i < len(spans) else "") + part
    return out


def _convert_latin_digits(text, table):
    count = [0]

    def repl(m):
        tok = m.group(0)
        if re.search(r"[A-Za-z]", tok):
            return tok
        new = tok.translate(table)
        if new != tok:
            count[0] += sum(ch.isdigit() for ch in tok)
        return new

    return _ALNUM_TOKEN.sub(repl, text), count[0]


def _quotes_to_guillemets(text):
    n = 0
    text, c = re.subn("“", "«", text)  # left curly  -> «
    n += c
    text, c = re.subn("”", "»", text)  # right curly -> »
    n += c
    out, opening = [], True
    for ch in text:
        if ch == '"':
            out.append("«" if opening else "»")
            opening = not opening
            n += 1
        else:
            out.append(ch)
    return "".join(out), n


def normalize(text, digits="persian"):
    """Return (fixed_text, stats); stats maps rule-name -> count."""
    stats = {}

    def bump(name, c):
        if c:
            stats[name] = stats.get(name, 0) + c

    masked, spans = _mask(text)

    for src, dst in CHAR_MAP.items():
        masked, c = re.subn(re.escape(src), dst, masked)
        bump("arabic_to_persian_letters", c)
    masked, c = re.subn(KASHIDA, "", masked)
    bump("kashida_removed", c)

    if digits == "persian":
        masked, c = re.subn("[٠-٩]", lambda m: m.group(0).translate(ARABIC_TO_FA), masked)
        bump("digits_to_persian", c)
        masked, c = _convert_latin_digits(masked, LATIN_TO_FA)
        bump("digits_to_persian", c)
    elif digits == "latin":
        masked, c = re.subn("[۰-۹]", lambda m: m.group(0).translate(FA_TO_LATIN), masked)
        bump("digits_to_latin", c)
        masked, c = re.subn("[٠-٩]", lambda m: m.group(0).translate(ARABIC_TO_LATIN), masked)
        bump("digits_to_latin", c)

    masked, c = re.subn(r"(?<![0-9۰-۹]),(?![0-9۰-۹])", "،", masked)
    bump("comma_to_persian", c)
    masked, c = re.subn(r";", "؛", masked)
    bump("semicolon_to_persian", c)
    masked, c = re.subn(r"\?", "؟", masked)
    bump("question_mark_to_persian", c)
    masked, c = _quotes_to_guillemets(masked)
    bump("quotes_to_guillemets", c)

    masked, c = re.subn(r"(^|[\s«»(){}\[\]\"'،؛؟.!:])(نمی|می)[ \t]+(?=\S)",
                        r"\1\2" + ZWNJ, masked)
    bump("zwnj_mi_prefix", c)
    masked, c = re.subn(r"(\S)[ \t]+(" + "|".join(HA_SUFFIXES) + r")(?=[\s،؛؟.!:»)\]]|$)",
                        r"\1" + ZWNJ + r"\2", masked)
    bump("zwnj_plural_ha", c)
    masked, c = re.subn(r"(\S)[ \t]+(ترین)(?=[\s،؛؟.!:»)\]]|$)",
                        r"\1" + ZWNJ + r"\2", masked)
    bump("zwnj_superlative", c)

    masked, c = re.subn(r"[ \t]+([،؛؟!.:»])", r"\1", masked)
    bump("space_before_punct", c)
    masked, c = re.subn(r"(«)[ \t]+", r"\1", masked)
    bump("space_after_openquote", c)
    masked, c = re.subn(r"([،؛؟!])(?=[^\s»)\]\x00])", r"\1 ", masked)
    bump("space_after_punct", c)
    masked, c = re.subn(r"[ \t]{2,}", " ", masked)
    bump("collapsed_spaces", c)
    masked, c = re.subn(r"[ \t]+(\n|$)", r"\1", masked)
    bump("trailing_space", c)

    return _unmask(masked, spans), stats


def suggestions(text):
    """Ambiguous cases we DETECT but never auto-fix."""
    out = []
    masked, _ = _mask(text)
    for m in re.finditer(r"(\S)[ \t]+(تر)(?=[\s،؛؟.!:»)\]]|$)", masked):
        out.append({"type": "maybe_comparative_tar",
                    "hint": "space+«تر»: join as «‌تر» if comparative; leave if it means 'wet'.",
                    "context": m.group(0)})
    for m in re.finditer(r"(?:^|[\s«»(){}\[\]\"'،؛؟.!:])(می|نمی)[آ-ی]", masked):
        out.append({"type": "maybe_glued_mi",
                    "hint": "«می» glued to verb: insert ZWNJ (می‌…); not auto-fixed (cf. «میمون»).",
                    "context": m.group(0)})
    return out


def line_changes(original, fixed):
    o, f = original.split("\n"), fixed.split("\n")
    return [{"line": i, "before": a, "after": b}
            for i, (a, b) in enumerate(zip(o, f), start=1) if a != b]


def _read(path):
    if path and path != "-":
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    return sys.stdin.read()


def main(argv=None):
    p = argparse.ArgumentParser(description="Deterministic Persian text mechanics linter/fixer.")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="report issues only (default)")
    mode.add_argument("--fix", action="store_true", help="output normalized text")
    p.add_argument("--in-place", action="store_true", help="with --fix, rewrite the file")
    p.add_argument("--json", action="store_true", help="machine-readable report (with --check)")
    p.add_argument("--digits", choices=["persian", "latin", "keep"], default="persian")
    p.add_argument("file", nargs="?", default="-", help="input file (default stdin)")
    a = p.parse_args(argv)

    text = _read(a.file)
    fixed, stats = normalize(text, digits=a.digits)
    sugg = suggestions(text)

    if a.fix:
        if a.in_place and a.file != "-":
            with open(a.file, "w", encoding="utf-8") as fh:
                fh.write(fixed)
            print("fixed: %s (%d changes)" % (a.file, sum(stats.values())), file=sys.stderr)
        else:
            sys.stdout.write(fixed)
        return 0

    changes = line_changes(text, fixed)
    if a.json:
        print(json.dumps({"stats": stats, "changes": changes, "suggestions": sugg},
                         ensure_ascii=False, indent=2))
    else:
        total = sum(stats.values())
        if not total and not sugg:
            print("clean - no mechanics issues found.")
        else:
            print("persian_lint: %d auto-fixable change(s) across %d line(s)\n" % (total, len(changes)))
            for rule, n in sorted(stats.items(), key=lambda kv: -kv[1]):
                print("  %4d  %s" % (n, rule))
            for ch in changes[:40]:
                print("\n  line %d:" % ch["line"])
                print("    - " + ch["before"])
                print("    + " + ch["after"])
            if sugg:
                print("\n  %d suggestion(s) needing human judgment:" % len(sugg))
                for s in sugg[:20]:
                    print("    ? %s: ...%s...  %s" % (s["type"], s["context"], s["hint"]))
    return 1 if (sum(stats.values()) or sugg) else 0


if __name__ == "__main__":
    raise SystemExit(main())
