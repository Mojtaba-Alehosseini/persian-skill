# persian: a Claude skill for Persian (Farsi) translation and text mechanics

Makes Claude translate English ↔ Persian the way a good human translator does (idiomatic,
register-matched, faithful, and free of the ChatGPT fingerprint), and fixes the small mechanical
things that make Persian look right: right-to-left layout, the half-space (ZWNJ / نیم‌فاصله),
Persian letters instead of their Arabic look-alikes, Persian digits, and proper punctuation.

It also works without translating. Point it at messy Persian and it cleans it up. Point it at
Persian that "sounds like AI" and it rewrites it.

There is a portable version for ChatGPT, Gemini, and any other assistant in [`portable/`](portable/).

## Install

Pick one. Most people want the first.

### 1. Claude app or claude.ai (upload a zip)

1. Download `persian.zip` from the [Releases](https://github.com/Mojtaba-Alehosseini/persian-skill/releases)
   page, or take it from whoever sent you here. The zip must contain a folder named `persian` with
   `SKILL.md` inside it. (GitHub's green "Code → Download ZIP" button gives you a folder named
   `persian-skill-main`, which Claude rejects because the folder name must match the skill name.
   Rename that folder to `persian` and re-zip it if that's what you have.)
2. In Claude, go to **Settings → Capabilities** and make sure **Code execution and file creation**
   is on. Skills need it.
3. Go to **Customize → Skills**, click **+**, then **Create skill → Upload a skill**, and pick the zip.
4. Toggle the skill on. Then ask normally: "translate this to Persian", "fix the نیم‌فاصله in this
   text", "make this Persian sound less like ChatGPT".

The same upload works for Cowork and the desktop app, since they read the skills on your claude.ai
account.

### 2. Claude Code (copy the folder)

Put the skill folder at `~/.claude/skills/persian/` (on Windows: `%USERPROFILE%\.claude\skills\persian\`).

```
git clone https://github.com/Mojtaba-Alehosseini/persian-skill ~/.claude/skills/persian
```

Claude Code picks it up on the next session. Note that Cowork and cloud sessions don't read this
folder; for those, use option 1.

### 3. ChatGPT, Gemini, or any other assistant (paste a prompt)

Open [`portable/PERSIAN-PROMPT.md`](portable/PERSIAN-PROMPT.md) and paste it into the instructions
of a Custom GPT, a ChatGPT Project, a Gemini Gem, or a Claude Project. It is under 8,000 characters,
which is the Custom GPT limit. For the small "custom instructions" box (1,500 characters on free
ChatGPT), use [`portable/PERSIAN-PROMPT-short.txt`](portable/PERSIAN-PROMPT-short.txt). The portable
version has no scripts, so the model applies the mechanics rules itself; it is a little less strict
than the linter but covers the same ground.

## نصب (به فارسی)

این مهارت (skill) به کلود یاد می‌دهد فارسی را مثل یک مترجم حرفه‌ای بنویسد، نه مثل ماشین: نیم‌فاصله‌ها
درست باشد، «ی» و «ک» فارسی باشد نه عربی، اعداد فارسی باشد، و متن بوی ترجمهٔ ماشینی یا «چت‌جی‌پی‌تی» ندهد.

نصب در کلود:

۱. فایل `persian.zip` را بگیرید (از صفحهٔ Releases یا از کسی که این لینک را برایتان فرستاده).
۲. در کلود به **Settings → Capabilities** بروید و **Code execution and file creation** را روشن کنید.
۳. به **Customize → Skills** بروید، روی **+** و بعد **Create skill → Upload a skill** بزنید و فایل zip را انتخاب کنید.
۴. مهارت را روشن کنید. حالا فقط بنویسید: «این را به فارسی ترجمه کن» یا «نیم‌فاصله‌های این متن را درست کن».

برای چت‌جی‌پی‌تی یا جمینای، متن فایل `portable/PERSIAN-PROMPT.md` را در بخش Instructions بچسبانید.

## What it does differently

Most "Persian mode" output reads like machine Persian: word-for-word calques, passive «شد» where
Persian uses an active verb, Arabic ي and ك, missing half-spaces, Latin digits, and the officialese
that models learned from government websites («می‌باشد», «مورد استفاده قرار می‌گیرد»). This skill
works on both halves:

- **Craft:** 56 rules derived from real differences between model drafts and published
  professional translations (Ghabraei, Haghighat), a catalog of AI-Persian tells, register
  guidance, and a review pass with back-translation for fidelity.
- **Mechanics:** a deterministic linter (`persian_lint.py`) that normalizes letters, ZWNJ, digits,
  punctuation, and spacing. It is idempotent, protects code and URLs, leaves English inside a
  Persian document alone, and flags ambiguous cases instead of guessing.

Examples:

```
in:  او مي رود و كتاب ها روي ميز است ، و بزرگ ترين آرزو همين بود 1964 .
out: او می‌رود و کتاب‌ها روی میز است، و بزرگ‌ترین آرزو همین بود ۱۹۶۴.
```

```
EN:  Teachers were dragged out and shot.
✗    معلم‌ها بیرون کشیده شدند و تیرباران شدند.      (calqued passive)
✓    معلم‌ها را بیرون کشیدند و تیرباران کردند.        (Persian impersonal active)
```

```
✗    این کتاب دارای سه فصل می‌باشد و توسط او نوشته شده است.   (officialese, AI tell)
✓    این کتاب سه فصل دارد و نوشتهٔ اوست.
```

When it writes a Word, PDF, or HTML file it sets RTL direction, start (visually right) alignment,
and a Persian-capable font, so the page looks native rather than "Persian text on a left-aligned page".

## What's inside

```
persian/
├── SKILL.md                     workflow, routing (translate / clean / write / look up), checklists
├── references/
│   ├── pitfalls.md              56 machine-Persian rules + worked EN↔FA exemplars
│   ├── ai-tells.md              signs of AI-written Persian and how to remove them
│   ├── typography-and-rtl.md    RTL, ZWNJ, digits, punctuation, file rendering
│   ├── register-guide.md        choosing and holding register; spoken vs written dialogue
│   ├── review-lenses.md         review lenses, priority order, verification checklist
│   └── lexicon.md               idioms, collocations, never-soften list, opt-in coinages
├── scripts/
│   ├── persian_lint.py          the mechanics linter (Python standard library only)
│   ├── lookup.py                builds a terminology brief from the banks
│   ├── test_scripts.py          regression tests
│   └── data/{idioms,glossary}.tsv
├── evals/evals.json             test prompts with checkable assertions
└── portable/                    prompt versions for ChatGPT / Gemini / Claude Projects
```

The scripts need Python 3.7 or newer and nothing else.

```
python scripts/persian_lint.py --fix messy.txt            # cleaned text to stdout
python scripts/persian_lint.py --check --style draft.txt  # report, including officialese flags
python scripts/test_scripts.py                            # run the tests
```

## Extending the term banks

`scripts/data/idioms.tsv` and `glossary.tsv` are small hand-curated seeds (format:
`EN <TAB> FA <TAB> note`). Add rows to grow coverage; `lookup.py` surfaces only the entries that
appear in a given source text, so the banks can scale without bloating context. `NOTICE` lists
open-source banks you can ingest and their licenses.

## Contributing

Issues and pull requests are welcome, especially new pitfalls with a real source, gold exemplars,
term and idiom rows, and Persian AI tells you keep seeing. Run `python scripts/test_scripts.py`
before submitting.

## License

MIT. See [LICENSE](LICENSE).
