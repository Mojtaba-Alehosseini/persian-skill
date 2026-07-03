# typography-and-rtl.md — Persian text mechanics (Pillar B reference)

The deterministic parts are enforced by `scripts/persian_lint.py`. This file explains the
rules behind it, and — importantly — the cases the script intentionally leaves to your judgment.
Run the script on any Persian you produce:

    python scripts/persian_lint.py --check file.txt
    python scripts/persian_lint.py --fix   file.txt

## 1. Letters — use Persian, not Arabic
Persian and Arabic share a script but differ in a few letters. Mixed text is the most common
encoding tell (it comes from Arabic keyboards, copy-paste, and old PDFs).

| Wrong (Arabic) | Right (Persian) | Note |
|---|---|---|
| ي  U+064A | ی  U+06CC | yeh — the #1 offender |
| ك  U+0643 | ک  U+06A9 | kaf |
| ى  U+0649 | ی  U+06CC | alef maksura → yeh |
| ة  U+0629 | ه  U+0647 | teh marbuta → heh (علاقه, not علاقة) |
| kashida ـ U+0640 | (delete) | decorative elongation; never in digital text |

Persian-only letters پ چ ژ گ (and ک ی) are correct — never "normalize" them to Arabic.
Leave intentional diacritics/harakat alone, and the linter preserves tanwin too (e.g. «بعداً», «مثلاً») rather than stripping it.

## 2. ZWNJ — نیم‌فاصله (half-space, U+200C)
ZWNJ joins a suffix/prefix to its stem *visually* without a full space. Getting this wrong
("میرود" glued, or "می رود" with a full space) is the clearest sign of unpolished Persian.

Required (the linter auto-fixes the space→ZWNJ cases):
- verb prefixes: می‌رود، نمی‌خواهم  (not «می رود» / «میرود»)
- plural/clitic ها: کتاب‌ها، خانه‌های، بچه‌هایش
- comparative/superlative: بزرگ‌تر، بزرگ‌ترین
- enclitic pronouns after a silent-heh/long vowel: خانه‌ام، خانه‌ات، خانه‌اش
- nominal -ها/-تر chains generally

Do NOT insert ZWNJ between genuinely separate words. Ambiguous cases the linter only *flags*:
- bare «تر» with a space — join if it is the comparative suffix, leave if it is the word "wet"
  (e.g. «زمینِ تر» = wet ground).
- a glued «میX» — usually needs می‌X, but not when «می» is part of a real word (میز, میمون, میهن).

## 3. Digits
Persian digits: ۰ ۱ ۲ ۳ ۴ ۵ ۶ ۷ ۸ ۹.
- Default policy: convert Latin (0-9) and Arabic-Indic (٠-٩) digits to Persian in prose.
- Keep Latin digits inside code spans, URLs, emails, and version numbers (`v1.2.3`, `2.4.1`).
  A token mixing letters and digits (MP3, COVID-19, iPhone15) keeps Latin digits.
- Separators: Persian thousands = ٬ (U+066C), decimal = ٫ (U+066B), percent = ٪.
  The linter is conservative: it converts the digits but leaves a Latin thousands comma and a
  decimal dot in place (so it never mangles `1,000` or a version). If you want true Persian
  separators (۱٬۰۰۰ / ۹۸٫۶), apply them by hand.
- Override globally with `--digits {persian,latin,keep}`.
- Units (feet→متر, °F→°C) are NOT a digit task — that is a translation decision; ask the user.

## 4. Punctuation & spacing
- Quotes: «…» (guillemets), not "…" or “…”.
- Comma «،», semicolon «؛», question mark «؟». Period and «!» share the Latin glyph.
- Spacing: no space *before* ، ؛ ؟ ! . : » and none *after* «; exactly one space *after*
  ، ؛ ؟ !. Collapse multiple spaces; strip trailing spaces.
- The linter handles all of the above.

## 5. Bidirectional (RTL) layout — the "small things"
Persian runs right-to-left, but numbers, Latin words, and some punctuation are left-to-right.
Where the two meet, glyphs can render on the visually wrong side. This is layout, not characters,
so the linter can't fully fix it — handle it consciously:

- A number or Latin run inside Persian keeps its own LTR order; that is correct. Don't reorder
  digits.
- Parentheses/brackets mirror automatically in a proper RTL renderer: type «(۲۰۲۰)» logically and
  it displays correctly. If a bracket or digit lands at a boundary and renders on the wrong side
  (common in plain-text fields, chat, code comments), insert a directional mark:
  RLM U+200F (right-to-left mark) after a trailing Latin/number, or LRM U+200E to isolate an
  LTR run. Use sparingly, only to fix a visible glitch.
- Keep punctuation that belongs to the Persian sentence (، ؛ ؟) in Persian form so the engine
  treats it as RTL and it sits on the correct side.
- For mixed Persian+English UI strings, prefer wrapping the Latin span rather than trusting
  auto-detection.

## 6. Dates & calendars
- Iran uses the Jalali (Hijri-Shamsi) calendar. When a date's calendar matters, state it or
  convert explicitly; don't silently assume Gregorian.
- Write dates with Persian digits in prose (۱۴۰۳/۳/۲۷ or ۲۷ خرداد ۱۴۰۳).

## 7. What the linter does vs. leaves to you
| Deterministic (linter) | Needs judgment (you) |
|---|---|
| ي/ك/ى/ة → Persian, kashida removal | bidi marks for a visible glitch |
| digit conversion + protected spans | true ٬ / ٫ separators |
| ، ؛ ؟ «», spacing | comparative «تر» vs "wet"; glued «می» |
| ZWNJ for می/نمی, ها, ترین | ZWNJ for rarer enclitic chains |
| — | unit conversion (ask the user) |

## 8. Rendering Persian in files (RTL + alignment + font)
The linter fixes characters; a *file* also needs direction, alignment, and a Persian font. Apply all
three to every Persian document you generate. **RTL without right-alignment still looks wrong.**

**Defaults:** direction = RTL · alignment = **start / leading** (visually right; not justified unless asked) ·
font = **Arial**, set as the complex-script font. Arial ships with Windows/Office and renders Persian, so it
needs no install and won't be substituted. For a nicer face (IRANSans, Vazirmatn), use one readers have or embed it.

**docx (docx-js):** set the font on ascii/hAnsi **and** `cs` (complex script), and align right:
```js
new Paragraph({
  bidirectional: true,                 // RTL direction
  alignment: AlignmentType.START,      // LOGICAL leading edge = visually right for RTL
  children: [ new TextRun({
    text, rightToLeft: true,
    font: { ascii: 'Arial', hAnsi: 'Arial', cs: 'Arial' },        // cs = the Persian (complex-script) font
  }) ],
});
```
If the toolkit won't emit `w:cs`, post-process `word/document.xml` to add `w:cs="Arial"` to each
`<w:rFonts>` — otherwise Word renders the Persian in its default CS font, ignoring your choice.

**Alignment gotcha (important):** in a bidi/RTL paragraph, Word reads `w:jc` *logically* — `left`=`start`,
`right`=`end`. So `w:jc="right"` is the *trailing* edge = the LEFT for RTL, and your text jumps left
(LibreOffice reads it physically, so it looks fine there — the bug only shows in Word). Always align RTL
text with the leading edge: `w:jc="start"` (docx-js `AlignmentType.START`). Never `right` for RTL.

**HTML/CSS:**
```css
body { direction: rtl; text-align: right;
       font-family: Arial,'IRANSans','Vazirmatn',Tahoma,sans-serif; }
```
**python-docx:** set `paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT`, `paragraph_format` bidi via the
XML `<w:bidi/>`, and the run's `w:rFonts w:cs='Arial'` (python-docx: `run.font.cs` is not exposed —
set it on the run's `rPr` XML directly).
