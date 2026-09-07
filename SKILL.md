---
name: persian
description: "Translate English↔Persian (Farsi) so it reads like a human translator, and fix Persian text mechanics: RTL, ZWNJ (نیم‌فاصله), ی/ک vs ي/ك, digits, punctuation. Use for any Persian text task."
---

# persian

Use this skill whenever the user wants text translated to or from Persian (Farsi), asks for a
Persian version of anything, wants Persian that doesn't sound machine-translated or "like
ChatGPT", or needs Persian text cleaned up (RTL, نیم‌فاصله, Arabic letters, digits, punctuation).
Also apply it whenever you write Persian yourself, even if nobody said "translate".

Two jobs:

- **Craft.** Render EN↔FA so it reads like a skilled human translator: idiomatic, register-matched,
  complete, faithful. Also: remove the fingerprint of AI-written Persian.
- **Mechanics.** The small things that make Persian look right regardless of word choice: RTL,
  ZWNJ, correct ی/ک, digits, punctuation, spacing.

Mechanics are deterministic, so they live in a script (`scripts/persian_lint.py`). Craft is
judgment, so it lives in this file and the references. Any Persian you emit should pass the linter
and respect the craft rules.

## Routing: pick the task first

| The user wants… | Route | Do this |
|---|---|---|
| English → Persian translation | **A** | full workflow below |
| Persian → English translation | **B** | reverse workflow |
| "fix / clean up / normalize this Persian", RTL, نیم‌فاصله, encoding | **C** | `persian_lint.py` only, no translation |
| write, edit, or review Persian; "make it sound human / not like AI" | **D** | craft rules + `references/ai-tells.md`, then the linter |
| "what's the natural Persian for X", an idiom or term | **E** | `lookup.py` and `references/lexicon.md` |

Routes C and D work standalone. You don't need a translation task to fix or improve Persian.

## Route A: English → Persian

For a single short line, translate directly and run the linter. The phases below pay off on
anything longer or important.

**1. Prep.** Read the source. Name its register (literary, contemporary dialogue, nonfiction,
official, children's) and audience; see `references/register-guide.md`. Build a terminology brief
with `python scripts/lookup.py <source_file>` (`--json` for structured output); it surfaces only the
idioms and collocations that occur in this text. If the text has measurements, settle the unit
policy with the user before drafting (see Numbers and units).

**2. Draft.** Write the full draft, applying the brief and the checklist below. When a structure is
tricky, open `references/pitfalls.md` (56 rules with worked EN↔FA exemplars).

**3. Review.** Run the lenses in `references/review-lenses.md`: back-translation (fidelity),
terminology, diction-grammar, ai-tells, fluency, modern standards, read-aloud. Parallel subagents if
you have them, inline otherwise.

**4. Synthesis.** Merge the feedback in this priority (highest wins): meaning fidelity →
terminology → grammar → no AI tells → oral fluency → register → modern accessibility → taste.

**5. Delivery.** Run `python scripts/persian_lint.py --fix` on the Persian. Run the verification
check. Deliver only the final translation plus two or three sentences on the choices that matter.
No drafts, lens reports, or back-translations unless asked.

**Route B (Persian → English)** reverses this: draft the English, review for English quality and
fidelity, skip the linter (the output is English). Still run `lookup.py --reverse` for consistent
terminology and still verify names and numbers.

## The machine-Persian checklist

The highest-frequency ways a draft betrays itself. Apply while drafting; the full catalog is in
`references/pitfalls.md`, and the AI-style layer is in `references/ai-tells.md`.

- **Passive → impersonal active (P32).** English agentless passive becomes Persian third-plural
  active, not «… شد». *were shot* → «… را … کشتند». Check every passive; this is the most common tell.
- **No it-clefts (P1).** "It's X that Y" → plain S-O-V. Don't calque «این … است که …».
- **-ing participles → coordinate verbs (P15).** Not «در حالِ …»: *ran the water, soaking the
  knife* → «شیر را باز کرد و چاقو را در آب گذاشت».
- **Dialogue must sound spoken (P8).** Match the speaker: *"Go on, now"* → «برو دیگه، یالا».
- **Drop implied words (P2).** *wedding night* → «عروسی».
- **«چرا» answers a negative question (P35).** *Isn't it…?* answered yes → «چرا، هست».
- **Verb-final order (P6).** *Upstairs was my room* → «اتاقم … در طبقهٔ بالا بود».
- **Persian collocations (P12, P13).** *the lights went out* → «برق رفت»; *perfect timing* → «چه به‌موقع!».
- **Flatten dialogue tags (P20).** suggested / conceded / announced → usually «گفت».
- **Re-segment to Persian rhythm (P5).** Shorter clauses; don't keep English dashes or clause order.
- **No officialese (ai-tells §1).** «است» not «می‌باشد»; «سه اتاق دارد» not «دارای سه اتاق است»;
  «استفاده می‌شود» not «مورد استفاده قرار می‌گیرد»; active, not «توسط».
- **No calqued «یک» (ai-tells §2).** *a good teacher* → «معلم خوبی است», not «یک معلم خوب است».
- **No English AI shape.** No rule-of-three, no «نه تنها … بلکه» every paragraph, no piled
  «همچنین / علاوه بر این», no em dash, no closing moral, no «لازم به ذکر است».

## Persian text mechanics

Finish every piece of Persian by running the linter:

    python scripts/persian_lint.py --check  file.txt          # report issues
    python scripts/persian_lint.py --fix    file.txt          # normalized text to stdout
    python scripts/persian_lint.py --check --style file.txt   # also flag officialese / AI phrases

It fixes Arabic → Persian letters (ي→ی, ك→ک, ة→ه, ى→ی), kashida, digits, punctuation
(, → «،», ; → «؛», ? → «؟», quotes → «…»), ZWNJ for می/نمی + ها + ترین + heh enclitics, and
spacing. It protects code, URLs, emails, and version numbers, and it converts punctuation only
where a Persian character sits next to it, so English inside a Persian document is untouched. It
is idempotent. Ambiguous cases (a bare «تر» that might mean "wet", a glued «میرود», an em dash) are
reported, never auto-changed; resolve those with judgment.

If you cannot run scripts, apply sections 1 to 4 of `references/typography-and-rtl.md` by hand:
ZWNJ for می‌/نمی‌، ‌ها، ‌تر/‌ترین and enclitics; «…» for quotes; «،» «؛» «؟»; Persian digits in prose.

### Numbers, digits, and units
- **Digits:** Persian (۰–۹) in prose; Latin inside code, URLs, and version numbers. The linter does
  this. Override with `--digits {persian,latin,keep}` when asked.
- **Units:** converting imperial → metric (feet → متر, °F → °C) changes meaning, so it is a
  translation decision, not a mechanics one. Offer: (a) metric, (b) original units, (c) both
  (original plus metric in parentheses). When the user hasn't said and the text has meaningful
  measurements, ask before delivering. The linter never touches units.

## Rendering Persian in files (docx, PDF, HTML, slides)

Characters aren't enough; the layout must be Persian too. Apply all three:

1. **Direction RTL.** docx: `bidirectional: true`; HTML: `dir="rtl"` and `lang="fa"`.
2. **Alignment: leading edge (logical start).** Do not set physical `right`: under bidi, Word reads
   `w:jc="right"` as the trailing edge and flips the text to the left. Use `w:jc="start"` (docx-js
   `AlignmentType.START`); CSS `text-align: start`.
3. **Font: Arial by default,** set as the complex-script font too (Word's `w:cs`), or the Persian
   glyphs ignore your choice. Vazirmatn or IRANSans if the readers have them or you embed them.

Run the linter on the text before placing it in the file. Snippets: `references/typography-and-rtl.md` §8.

## Verification check (before delivering a translation)

- **Complete and faithful.** Full meaning, nothing omitted, added, or softened. Alcohol, sex,
  politics, religion: translate as written. Published Iranian editions cut these; you don't.
- **Checked against the source:** proper nouns, place names, numbers, dates, unit conversions,
  polarity and quantifiers. The back-translation lens is the fastest way to catch a shifted meaning.

## Reference index

Read on demand, not all up front.

| File | When to read |
|---|---|
| `references/pitfalls.md` | drafting EN→FA; 56 machine-Persian rules with worked exemplars |
| `references/ai-tells.md` | route D; the ai-tells lens; anything that "sounds like ChatGPT" |
| `references/typography-and-rtl.md` | RTL, ZWNJ, punctuation, digits, file rendering, what the linter leaves to you |
| `references/register-guide.md` | choosing register; spoken vs written dialogue |
| `references/review-lenses.md` | Phase 3 lenses, priority order, verification checklist |
| `references/lexicon.md` | idioms, collocations, never-soften list, opt-in house-style coinages |

Paths are relative to the skill root (the folder holding this file); run scripts from there.
Scripts: `scripts/persian_lint.py`, `scripts/lookup.py`. Data: `scripts/data/{idioms,glossary}.tsv`,
never loaded into context. Tests: `python scripts/test_scripts.py`.
