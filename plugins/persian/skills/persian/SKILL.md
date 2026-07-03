---
name: persian
description: >-
  Translate between English and Persian (Farsi) at professional, idiomatic quality,
  and fix Persian text mechanics — right-to-left/RTL, ZWNJ (نیم‌فاصله / half-space),
  Arabic-vs-Persian letters (ي/ك → ی/ک), digits, and punctuation («» ، ؛ ؟). Use this
  skill whenever the user wants to translate to or from Persian/Farsi, asks for a Persian
  version of any text, wants their Persian to sound natural instead of "machine-translated,"
  or needs to clean up, normalize, or fix the formatting/encoding of Persian text — even if
  they don't explicitly say "translate" or "RTL." Also apply it whenever you generate Persian
  output yourself, so the result avoids the common mistakes catalogued here.
---

# persian

A general-purpose Persian (Farsi) skill with two jobs:

- **Pillar A — Translation craft.** Render EN↔FA so it reads like a skilled human translator,
  not "machine Persian": idiomatic, register-matched, complete, and accurate to the source.
- **Pillar B — Persian text mechanics.** The "small things" that make Persian look right
  regardless of word choice: RTL, ZWNJ (نیم‌فاصله), correct ی/ک, digits, punctuation, spacing.

The architecture follows one idea: **mechanics are deterministic, so they live in a script**
(`scripts/persian_lint.py`); **craft is judgment, so it lives in this guide plus the reference
catalogs.** Anytime you emit Persian — translated or original — it should pass the linter and
respect the craft rules below.

---

## Routing — pick the task first

| The user wants… | Route | Do this |
|---|---|---|
| English → Persian translation | **A** | full translation workflow ↓ |
| Persian → English translation | **B** | reverse workflow ↓ |
| "fix / clean up / normalize this Persian", RTL, نیم‌فاصله, encoding | **C** | run `persian_lint.py` only — no translation |
| write or review Persian (no source to translate) | **D** | apply craft rules + finish with `persian_lint.py` |
| "what's the natural Persian for X" / idiom or term lookup | **E** | `lookup.py` and/or `references/lexicon.md` |

Routes C and D mean **Pillar B works standalone** — you do not need a translation task to fix
or improve Persian text.

---

## Route A — English → Persian (the main workflow)

Five phases. For a single short line, skip the team and translate directly; the phases pay off
on anything longer or important.

### Phase 1 — Prep
1. Read the source; name its **register** (literary / contemporary dialogue / nonfiction /
   children's / formal memoir …), audience, and purpose. Register drives every later choice —
   see `references/register-guide.md`.
2. Build a **terminology brief** — only the terms relevant to *this* text:
   `python scripts/lookup.py <source_file>` (use `--json` for structured output). The brief
   surfaces the idioms and collocations that occur in the text so the draft uses them.
3. If the text has measurements, settle the **unit policy** with the user before drafting
   (see *Numbers, digits & units*).

### Phase 2 — Draft
Produce your best full draft, applying the brief and the **machine-Persian checklist** below.
Reach into `references/pitfalls.md` when a structure is tricky — the full 56-pattern catalog, plus
its **Worked exemplars** section of aligned EN↔FA sentences.

### Phase 3 — Review (lenses)
Run the review lenses in `references/review-lenses.md`. For long or important texts, spawn them
as **parallel subagents** (one per lens); for short texts, run them inline. The lenses:
diction-grammar, fluency-eloquence, modern-standards, back-translation (the fidelity check),
oral/read-aloud, plus terminology-compliance.

### Phase 4 — Synthesis
Merge the feedback by this **conflict-resolution priority** (highest wins):
1. Meaning fidelity (back-translation) → 2. Terminology compliance → 3. Grammar →
4. Oral fluency → 5. Register & style → 6. Modern accessibility → 7. Aesthetic preference.

### Phase 5 — Delivery
1. Run `python scripts/persian_lint.py --fix` on the Persian so it is mechanically clean.
2. Run the **verification check** (below).
3. Deliver **only the final translation + a 2–3 sentence summary** of key choices. Do not dump
   drafts, lens reports, or back-translations unless asked.

**Route B (Persian → English)** reverses this: you draft the English, the lenses check English
quality and fidelity, and you skip the linter (the output is English). Still run `lookup.py
--reverse` to keep terminology consistent, and still verify names and numbers.

---

## The machine-Persian checklist (top tells)

These are the highest-frequency ways an EN→FA draft betrays itself. Apply them while drafting;
the full catalog is in `references/pitfalls.md`.

- **Passive → impersonal active (P32).** English agentless passive becomes Persian 3rd-plural
  active, not «… شد». *were shot* → «… را … کشتند» (not «کشته شدند»). Check **every** passive —
  the single most common tell.
- **Kill English it-clefts (P1).** "It's X that Y" → plain S-O-V. Don't calque «این … است که …».
- **-ing participles → coordinate finite verbs (P15).** Not «در حالِ …»: *ran the water, soaking
  the knife* → «شیر را باز کرد و چاقو را در آب گذاشت».
- **Dialogue must sound spoken (P8).** Flat literal dialogue is the #1 giveaway. Match the
  speaker: *"Go on, now"* → «بزن بِچاک. فوراً.»
- **Drop redundant/implied words (P2).** *wedding night* → «عروسی» (the «شب» is usually dropped).
- **«چرا» answers a negative question (P35).** *Isn't it…?* answered yes → «چرا، هست.» (not «بله»).
- **Predicate verb over a bare adjective string (P3).** *tired and grim* → «خسته و گرفته به نظر
  می‌رسید».
- **Verb-final order — don't mimic English fronting (P6).** *Upstairs was my room* →
  «اتاقِ خوابم … در طبقهٔ بالا بود».
- **Use the Persian collocation/stock phrase (P12/P13).** *the lights went out* → «برق رفت»;
  *perfect timing* → «چه به‌موقع!».
- **Flatten varied dialogue tags (P20).** suggested/conceded/announced → usually «گفت»; specify
  manner only when it matters.
- **Add affective particles where Persian colors emotion (P25).** *it must have been so hot* →
  «طفلکی … حتماً …».
- **Re-segment to Persian rhythm (P5).** Break long English periods into shorter Persian clauses;
  don't preserve English dashes/clause order.

When in doubt about a structure, read the matching P-rule in `references/pitfalls.md` and check its
**Worked exemplars** section for a worked example.

---

## Persian text mechanics (Pillar B)

Always finish Persian output by running the linter; it enforces these deterministically:

    python scripts/persian_lint.py --check  file.txt     # report issues
    python scripts/persian_lint.py --fix    file.txt     # normalized text to stdout
    cat file.txt | python scripts/persian_lint.py --fix  # stdin → stdout

What it fixes: Arabic→Persian letters (ي→ی, ك→ک, ة→ه, ى→ی), kashida removal, digit policy,
punctuation (`,`→`،`, `;`→`؛`, `?`→`؟`, straight/curly quotes→«…»), ZWNJ for می/نمی + ها +
ترین, and spacing around punctuation. It **protects** code spans, URLs, emails, and version
numbers (these keep Latin digits). It is safe and idempotent; ambiguous cases (a bare «تر» that
might mean "wet"; a glued «میرود») are reported as suggestions, never auto-changed — resolve
those with judgment.

Key rules worth knowing even without the script: use ZWNJ (نیم‌فاصله) for می‌/نمی‌, ‌ها, ‌تر/‌ترین,
and enclitics; quotes are «…» (guillemets); the comma is «،» and the question mark «؟». For the
full reference (including bidi handling of numbers/Latin inside RTL, dates, and the cases the
script intentionally leaves to you), read `references/typography-and-rtl.md`.

### Numbers, digits & units
- **Digits (default):** convert Latin/Arabic-Indic digits to Persian (۰–۹) in prose, but **keep
  Latin digits inside code, URLs, and version numbers** (e.g. `v1.2.3`). The linter does this.
  Override per request with `--digits {persian,latin,keep}`.
- **Units:** converting imperial→metric (feet→متر, °F→°C, per P19) changes meaning, so it is a
  **translation decision, not a mechanics one — ask the user.** Offer: (a) convert to metric,
  (b) keep original units, (c) keep both (original + metric in parentheses or a footnote). Apply
  their choice consistently. When the user hasn't said and the text has meaningful measurements,
  ask before delivering. The linter never touches units.

---

## Rendering Persian in files (docx / PDF / HTML) — layout is mechanics too

When you emit Persian into a **file**, the characters are not enough; the *layout* must be Persian
as well. Whenever you create a document, slide, or page with Persian body text, apply all three —
RTL alone is not enough:

1. **Direction: right-to-left.** Set paragraph/section direction to RTL (docx: `bidirectional: true`;
   HTML/CSS: `dir="rtl"` / `direction: rtl`).
2. **Alignment: leading edge (logical "start"), which is visually right for RTL.** Do NOT set physical
   `right`: Word treats `w:jc="right"` as the *trailing* edge under bidi and flips RTL text to the LEFT
   (a real, surprising gotcha). Use the logical start edge — docx `AlignmentType.START` (`w:jc="start"`),
   or in CSS `text-align: right`/`start`. Justify only if asked. RTL + start-align = native-looking page.
3. **Font: Arial by default.** Arial ships with Windows/Office and renders Persian, so it needs no
   install and won't be substituted. Set it as the **complex-script** font too — in Word the run's
   `w:cs` font, not only the Latin font — or the Persian glyphs ignore your choice. For a nicer Persian
   face (IRANSans, Vazirmatn), use a font you know readers have, or embed it in the file.

Persian digits, «», and ZWNJ still apply: run `persian_lint.py` on the text *before* placing it in the
file. Concrete docx/HTML snippets are in `references/typography-and-rtl.md` §8.

## Verification check (before delivering a translation)

- **Translate completely and accurately** — render the full meaning; don't omit, add, or soften
  content relative to the source.
- **Verify against the source:** proper nouns, place names, numbers, dates, and any unit
  conversions — these are where errors hide. The **back-translation** lens (see
  `references/review-lenses.md`) is the fastest way to catch a shifted or dropped meaning.
- Details and the checklist live in `references/review-lenses.md` (Verification checklist).

---

## Reference index

Read these on demand — do not load them all up front.

| File | When to read |
|---|---|
| `references/pitfalls.md` | drafting EN→FA; the machine-Persian catalog (56 rules) + worked EN↔FA exemplars |
| `references/typography-and-rtl.md` | any RTL / encoding / ZWNJ / punctuation / file-rendering question; what the linter leaves to judgment |
| `references/register-guide.md` | choosing register by text type |
| `references/review-lenses.md` | Phase 3 review; lens mandates, parallelizing, + the verification checklist |
| `references/lexicon.md` | idiom, term & collocation choices; house-style preferences |

**Paths in this skill are relative to the skill root** (the folder that holds this SKILL.md); run the scripts from there, e.g. `python scripts/persian_lint.py`.

Scripts: `scripts/persian_lint.py` (mechanics), `scripts/lookup.py` (terminology brief).
Data the scripts read: `scripts/data/{idioms,glossary}.tsv` — never loaded into context; extend
them to scale (see `NOTICE` for the open-source sources and licensing).
