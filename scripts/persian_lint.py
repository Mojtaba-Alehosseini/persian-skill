#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""persian_lint.py - deterministic Persian text mechanics normalizer / linter.

Part of the `persian` skill. Fixes the "small things" that make Persian text look
wrong no matter how good the word choice is: Arabic-vs-Persian letters, digits,
ZWNJ (نیم‌فاصله), punctuation, spacing, and kashida. None of this needs human
judgment, so it lives in code: repeatable, testable, fast. Stdlib only.

USAGE
    python persian_lint.py --check  file.txt        # report issues only (default)
    python persian_lint.py --fix    file.txt        # print fixed text to stdout
    python persian_lint.py --fix --in-place file.txt
    cat file.txt | python persian_lint.py --fix     # stdin -> stdout
    python persian_lint.py --check --json file.txt  # machine-readable report
    python persian_lint.py --check --style file.txt # also flag bureaucratic / AI-tell phrases

DIGIT POLICY (default = "persian")
    Convert Latin (0-9) and Arabic-Indic (٠-٩) digits to Persian (۰-۹) in prose,
    but NEVER inside code spans (``` ``` and `inline`), URLs, emails, or version
    numbers (v1.2.3, 2.4.1). A token that also has Latin letters (MP3, COVID-19,
    iPhone15) keeps Latin digits. Override with --digits {persian,latin,keep}.
    Unit conversion (feet->meters, F->C) is a translation decision, not a
    mechanics one. It is handled in the skill workflow (ask the user), never here.

MIXED TEXT
    Latin punctuation (, ; ? "…") is converted only where it belongs to Persian
    text (a Persian character next to it). An English sentence inside a Persian
    document keeps its own punctuation.

DESIGN
    Safe by default. High-confidence fixes are applied; ambiguous cases (a bare
    «تر» that might mean "wet"; a glued «میرود»; an em dash) are reported, never
    auto-changed. Running --fix twice gives the same result as running it once.
"""
import argparse
import json
import re
import sys

# Windows consoles default to a legacy code page; force UTF-8 on every stream.
for _stream in (sys.stdout, sys.stderr, sys.stdin):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

ZWNJ = "‌"     # نیم‌فاصله / zero-width non-joiner
KASHIDA = "ـ"  # tatweel
EN_DASH = "–"

CHAR_MAP = {
    "ي": "ی",  # ARABIC YEH    ي -> PERSIAN YEH ی
    "ى": "ی",  # ALEF MAKSURA  ى -> PERSIAN YEH ی
    "ك": "ک",  # ARABIC KAF    ك -> PERSIAN KEHEH ک
    "ة": "ه",  # TEH MARBUTA   ة -> HEH ه
}

LATIN_TO_FA = {ord(a): b for a, b in zip("0123456789", "۰۱۲۳۴۵۶۷۸۹")}
ARABIC_TO_FA = {ord(a): b for a, b in zip("٠١٢٣٤٥٦٧٨٩", "۰۱۲۳۴۵۶۷۸۹")}
FA_TO_LATIN = {ord(b): a for a, b in zip("0123456789", "۰۱۲۳۴۵۶۷۸۹")}
ARABIC_TO_LATIN = {ord(a): b for a, b in zip("٠١٢٣٤٥٦٧٨٩", "0123456789")}

# Persian/Arabic letters (not digits, not punctuation). Used as word boundaries.
PL = "ء-يٮ-ەۺ-ۼۿ"
# Letters plus harakat/tanwin (a word may end in a diacritic: «زمینِ»).
PLD = PL + "\u064b-\u0652\u0670"
# Anything that marks "this is Persian context": letters, Persian digits, ZWNJ.
AR = PL + "۰-۹٠-٩‌"

# Convert digits only when the WHOLE alnum token is digits -> MP3, COVID-19 keep Latin.
_ALNUM_TOKEN = re.compile(r"[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*")

# ZWNJ plural/clitic suffixes, LONGEST-FIRST so alternation prefers them.
HA_SUFFIXES = ["هایشان", "هایتان", "هایمان", "هایی", "هایم", "هایت", "هایش", "های", "ها"]
# Enclitics that attach to a word ending in silent heh: خانه‌ام، رفته‌اند، خانه‌ای
HEH_ENCLITICS = ["اند", "ایم", "اید", "ام", "ات", "اش", "ای"]
# Function words ending in ه that must never take a ZWNJ enclitic.
HEH_STOPWORDS = {"که", "چه", "نه", "به", "سه", "بله", "آنچه", "چنانچه", "اگرچه", "گرچه"}

# Never touch: fenced code, inline code, indented code lines, URLs, emails, version numbers.
_PROTECT = re.compile(
    r"```.*?```"
    r"|`[^`\n]*`"
    r"|^(?: {4,}|\t)\S.*$"
    r"|(?:https?://|www\.)\S+"
    r"|[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"
    r"|\bv\d+(?:\.\d+)+\b"
    r"|\b\d+\.\d+\.\d+\b",
    re.DOTALL | re.MULTILINE,
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


def _is_persian_line(line):
    """A line is Persian when it has more Persian letters than Latin letters."""
    fa = len(re.findall("[" + PL + "]", line))
    la = len(re.findall("[A-Za-z]", line))
    return fa > la


def _persian_neighbours(text, i):
    """True if the char right before position i is Persian AND the next non-space
    char is Persian: the punctuation sits inside Persian text."""
    if i == 0 or not re.match("[" + AR + "]", text[i - 1]):
        return False
    k = i + 1
    while k < len(text) and text[k] in " \t":
        k += 1
    return k < len(text) and re.match("[" + AR + "]", text[k]) is not None


def _convert_punct(line, latin, persian, persian_line, between_digits_ok=False):
    """Replace `latin` with `persian` where it belongs to Persian text: on a
    Persian-majority line, or when flanked by Persian on both sides."""
    out, n, i = [], 0, 0
    while i < len(line):
        ch = line[i]
        if ch == latin and (persian_line or _persian_neighbours(line, i)):
            prev_d = i > 0 and re.match(r"[0-9۰-۹]", line[i - 1])
            next_d = i + 1 < len(line) and re.match(r"[0-9۰-۹]", line[i + 1])
            if between_digits_ok or not (prev_d and next_d):
                out.append(persian)
                n += 1
                i += 1
                continue
        out.append(ch)
        i += 1
    return "".join(out), n


_QUOTE_PAIR = re.compile(r'"([^"\n]*)"|“([^“”\n]*)”')


def _quotes_to_guillemets(line, persian_line):
    """Convert a quote pair to «…» when it is Persian: the line is Persian, or the
    quoted content itself is Persian-majority."""
    n = [0]

    def repl(m):
        inner = m.group(1) if m.group(1) is not None else m.group(2)
        if persian_line or (inner.strip() and _is_persian_line(inner)):
            n[0] += 1
            return "«" + inner + "»"
        return m.group(0)

    return _QUOTE_PAIR.sub(repl, line), n[0]


# Markdown / plain-text list markers keep Latin digits ("1. item"), or the list
# stops rendering as a list.
_LIST_MARKER = re.compile(r"^(\s*)(\d+)([.)])(\s)")


def _convert_digits_line(line, table, persian_line, doc_persian):
    if not (persian_line or (doc_persian and not re.search("[A-Za-z]", line))):
        return line, 0
    m = _LIST_MARKER.match(line)
    head = ""
    if m:
        head, line = m.group(0), line[m.end():]
    line, c = _convert_latin_digits(line, table)
    return head + line, c


def _heh_enclitics(text):
    """خانه ام -> خانه‌ام ; رفته اند -> رفته‌اند ; skips function words (که ای)."""
    pat = re.compile(r"([" + PL + "]*ه)[ \t]+(" + "|".join(HEH_ENCLITICS) + r")(?![" + PL + "])")
    n = [0]

    def repl(m):
        word = m.group(1)
        if word in HEH_STOPWORDS or len(word) < 2:
            return m.group(0)
        n[0] += 1
        return word + ZWNJ + m.group(2)

    return pat.sub(repl, text), n[0]


def normalize(text, digits="persian"):
    """Return (fixed_text, stats); stats maps rule-name -> count."""
    stats = {}

    def bump(name, c):
        if c:
            stats[name] = stats.get(name, 0) + c

    masked, spans = _mask(text)

    # 1. Letters
    for src, dst in CHAR_MAP.items():
        masked, c = re.subn(re.escape(src), dst, masked)
        bump("arabic_to_persian_letters", c)

    # 2. Kashida: a spaced kashida is being used as a dash -> en dash; the rest is
    #    decorative elongation -> delete.
    masked, c = re.subn(r"(?:(?<=\s)|^)" + KASHIDA + r"+(?=\s|$)", EN_DASH, masked, flags=re.M)
    bump("kashida_dash_to_en_dash", c)
    masked, c = re.subn(KASHIDA, "", masked)
    bump("kashida_removed", c)

    # 3. Digits (Arabic-Indic digits are always wrong in Persian; Latin digits are
    #    converted only on Persian lines, or number-only lines of a Persian document)
    doc_persian = _is_persian_line(masked)
    if digits == "persian":
        masked, c = re.subn("[٠-٩]", lambda m: m.group(0).translate(ARABIC_TO_FA), masked)
        bump("digits_to_persian", c)
    elif digits == "latin":
        masked, c = re.subn("[۰-۹]", lambda m: m.group(0).translate(FA_TO_LATIN), masked)
        bump("digits_to_latin", c)
        masked, c = re.subn("[٠-٩]", lambda m: m.group(0).translate(ARABIC_TO_LATIN), masked)
        bump("digits_to_latin", c)

    # 4. Line-aware passes: digits, punctuation, quotes, spacing around Latin marks.
    lines = masked.split("\n")
    for idx, line in enumerate(lines):
        pl = _is_persian_line(line)
        if digits == "persian":
            line, c = _convert_digits_line(line, LATIN_TO_FA, pl, doc_persian)
            bump("digits_to_persian", c)
        line, c = re.subn(r"(?<=[۰-۹])%", "٪", line)
        bump("percent_to_persian", c)
        line, c = _convert_punct(line, ",", "،", pl)
        bump("comma_to_persian", c)
        line, c = _convert_punct(line, ";", "؛", pl, between_digits_ok=True)
        bump("semicolon_to_persian", c)
        line, c = _convert_punct(line, "?", "؟", pl, between_digits_ok=True)
        bump("question_mark_to_persian", c)
        line, c = _quotes_to_guillemets(line, pl)
        bump("quotes_to_guillemets", c)
        if pl:
            line, c = re.subn(r"(?<=\S)[ \t]+([.!:،؛؟»])", r"\1", line)
            bump("space_before_punct", c)
            line, c = re.subn(r"(!)(?=[^\s»)\]\x00،؛؟!.…])", r"\1 ", line)
            bump("space_after_punct", c)
        lines[idx] = line
    masked = "\n".join(lines)
    masked, c = re.subn(r"(?<=[" + PL + r"‌])\.{3,}", "…", masked)
    bump("ellipsis", c)

    # 5. ZWNJ (touches Persian letters only, so safe on any line)
    masked, c = re.subn(r"(?<![" + PL + r"‌])(نمی|می)[ \t]+(?=[" + PL + "])",
                        r"\1" + ZWNJ, masked)
    bump("zwnj_mi_prefix", c)
    masked, c = re.subn(r"(?<=[" + PLD + r"])[ \t]+(" + "|".join(HA_SUFFIXES) + r")(?![" + PL + "])(?! و هوی)",
                        ZWNJ + r"\1", masked)
    bump("zwnj_plural_ha", c)
    masked, c = re.subn(r"(?<=[" + PLD + r"])[ \t]+(ترین)(?![" + PL + "])",
                        ZWNJ + r"\1", masked)
    bump("zwnj_superlative", c)
    masked, c = _heh_enclitics(masked)
    bump("zwnj_heh_enclitic", c)

    # 6. Spacing around Persian punctuation (Persian characters, so safe anywhere)
    masked, c = re.subn(r"(?<=[" + AR + r"])[ \t]+([،؛؟»])", r"\1", masked)
    bump("space_before_punct", c)
    masked, c = re.subn(r"(«)[ \t]+", r"\1", masked)
    bump("space_after_openquote", c)
    masked, c = re.subn(r"([،؛؟])(?=[^\s»)\]\x00،؛؟!.…])", r"\1 ", masked)
    bump("space_after_punct", c)
    masked, c = re.subn(r"(?<=\S)[ \t]{2,}(?=\S)", " ", masked)
    bump("collapsed_spaces", c)
    masked, c = re.subn(r"[ \t]+(\n|$)", r"\1", masked)
    bump("trailing_space", c)

    return _unmask(masked, spans), stats


# Bureaucratic / machine-Persian phrases. Reported with --style, never auto-fixed:
# each one is sometimes right, and the fix needs a rewrite, not a substitution.
STYLE_FLAGS = [
    (r"می‌باشد|می‌باشند|میباشد", "«می‌باشد» -> «است / هستند»"),
    (r"می‌گردد|می‌گردند", "«می‌گردد» as a passive helper -> «می‌شود» or an active verb"),
    (r"مورد\s+\S+\s+قرار\s+(?:می‌گیرد|گرفت|گرفته|داد|می‌دهد)", "«مورد … قرار گرفتن» -> plain verb (استفاده می‌شود، بررسی کردند)"),
    (r"\bدارای\b", "«دارای X است» -> «X دارد»"),
    (r"\bتوسط\b", "«توسط» agent passive -> active sentence (او نوشت)"),
    (r"\bبه عنوان\b|\bبه‌عنوان\b", "«به عنوان» is often a calque of English 'as'; try dropping it"),
    (r"\bبه منظور\b|\bبه‌منظور\b|\bدر راستای\b|\bدر جهت\b", "bureaucratic connector -> «برای»"),
    (r"لازم به ذکر است|شایان ذکر است|قابل ذکر است|قابل توجه است که", "announcement filler; delete it and state the point"),
    (r"نه تنها .{0,60}? بلکه", "«نه تنها … بلکه» is over-used by models; try a plain sentence"),
    (r"\bدر نهایت\b|\bدر پایان\b|\bبه طور کلی\b|\bدر مجموع\b", "summary connector; usually delete"),
    (r"\bاین امر\b|\bاین موضوع\b|\bاین مسئله\b", "abstract subject; name the concrete thing"),
    (r"\bایفا می‌کند\b|\bنقش (?:مهم|کلیدی|حیاتی)", "«نقش مهمی ایفا می‌کند» is the Persian 'plays a crucial role'; say what it does"),
    (r"\bیک\s+\S+ی?\s+است\b", "«یک X است» often calques English 'a'; Persian usually says «Xی است» or just «X است»"),
]

# Real words that start with «می» and are NOT the verb prefix; never flagged as glued.
MI_WORDS = {"میز", "میزان", "میزبان", "میان", "میانه", "میانگین", "میانبر", "میدان", "میوه",
            "میهن", "میهمان", "میمون", "میل", "میلاد", "میلادی", "میلیون", "میلیارد", "میله",
            "میخ", "میت", "میثاق", "میراث", "میکروب", "میکرو", "مینا", "مینو", "میش", "میگو",
            "میکده", "میکس", "میثم", "میرزا", "میر", "میگرن", "میناکاری", "میخانه", "میخک",
            "میدانی", "میلی", "میکروفون", "میکروسکوپ", "میکروفر", "میلیمتر", "میلی‌متر",
            "میانی", "میدانها", "میوه‌ها", "میزها", "میلها", "میخها", "میسر", "میکائیل",
            "میناب", "میامی", "میگل", "میلان", "میکل", "میکی", "میترا", "میثاق‌نامه"}


def suggestions(text, style=False):
    """Ambiguous cases we DETECT but never auto-fix."""
    out = []
    masked, _ = _mask(text)
    for m in re.finditer(r"(?<=[" + PLD + r"])[ \t]+(تر)(?![" + PL + "])", masked):
        out.append({"type": "maybe_comparative_tar",
                    "hint": "space+«تر»: join as «‌تر» if comparative; leave if it means 'wet'.",
                    "context": masked[max(0, m.start() - 12):m.end() + 3]})
    for m in re.finditer(r"(?<![" + PL + r"‌])((?:ن)?می[" + PL + "]+)", masked):
        word = m.group(1)
        stem = word[1:] if word.startswith("ن") else word
        if stem in MI_WORDS or stem.rstrip("ی") in MI_WORDS:
            continue
        out.append({"type": "maybe_glued_mi",
                    "hint": "«می» glued to verb: insert ZWNJ (می‌…); not auto-fixed (cf. «میمون», «میز»).",
                    "context": masked[max(0, m.start() - 3):m.end() + 3]})
    for m in re.finditer("—", masked):
        out.append({"type": "em_dash",
                    "hint": "em dash: Persian prose rarely uses it; restructure, or use a spaced en dash (–) if a dash is really needed.",
                    "context": masked[max(0, m.start() - 12):m.end() + 12].replace("\n", " ")})
    if style:
        for pat, hint in STYLE_FLAGS:
            for m in re.finditer(pat, masked):
                out.append({"type": "style",
                            "hint": hint,
                            "context": masked[max(0, m.start() - 15):m.end() + 15].replace("\n", " ")})
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
    p.add_argument("--style", action="store_true",
                   help="also flag bureaucratic / machine-Persian phrases (never auto-fixed)")
    p.add_argument("--digits", choices=["persian", "latin", "keep"], default="persian")
    p.add_argument("file", nargs="?", default="-", help="input file (default stdin)")
    a = p.parse_args(argv)

    text = _read(a.file)
    fixed, stats = normalize(text, digits=a.digits)
    sugg = suggestions(fixed if a.fix else text, style=a.style)

    if a.fix:
        if a.in_place and a.file != "-":
            with open(a.file, "w", encoding="utf-8") as fh:
                fh.write(fixed)
            print("fixed: %s (%d changes)" % (a.file, sum(stats.values())), file=sys.stderr)
        else:
            sys.stdout.write(fixed)
            sys.stdout.flush()
        if sugg:
            print("\n%d item(s) need judgment (run --check for details)" % len(sugg), file=sys.stderr)
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
                for s in sugg[:30]:
                    print("    ? %s: ...%s...  %s" % (s["type"], s["context"], s["hint"]))
    return 1 if (sum(stats.values()) or sugg) else 0


if __name__ == "__main__":
    raise SystemExit(main())
