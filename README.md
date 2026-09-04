# persian: Claude skill for Persian (Farsi) translation & text mechanics

Make Claude translate **English ↔ Persian** like a skilled human (idiomatic, register-matched, faithful) **and** fix the small mechanical things that make Persian look right: right-to-left layout, the half-space (ZWNJ / نیم‌فاصله), correct Persian letters instead of their Arabic look‑alikes, Persian digits, and proper punctuation.

> Two jobs in one skill: **translation craft** (judgment) + **Persian text mechanics** (deterministic, done by a script).

---

## Why it's different

Most "Persian mode" output reads like *machine Persian*: word-for-word calques, Arabic letters (ي/ك), missing half-spaces, Latin digits. This skill fixes both halves:

- **Craft**: a catalog of 56 calibrated pitfalls (passive→impersonal active, it‑clefts, dialogue register, collocations…) with worked EN↔FA examples and review "lenses."
- **Mechanics**: a deterministic linter (`persian_lint.py`) that normalizes letters, ZWNJ, digits, punctuation and spacing; safe and idempotent, and it protects code/URLs/version numbers.

It also works **without translating**: point it at messy Persian and it just cleans it up.

---

## Install

```
/plugin marketplace add Mojtaba-Alehosseini/persian-skill
/plugin install persian@persian-skill
```

Then just ask normally, for example "translate this to Persian," "fix the نیم‌فاصله in this text," or "what's the natural Persian for *it cost an arm and a leg*."

---

## Examples

**Fix Persian typography (no translation):**

```
in:  او مي رود و كتاب ها روي ميز است ، و بزرگ ترين آرزو همين بود 1964 .
out: او می‌رود و کتاب‌ها روی میز است، و بزرگ‌ترین آرزو همین بود ۱۹۶۴.
```

(ي→ی, ك→ک, ZWNJ added, digits → Persian, spacing around «،» fixed.)

**Idiomatic translation, not calque:**

```
EN:  "Go on, now," he said.
FA:  گفت: «بزن بِچاک.»        ← spoken register, not «برو دیگر، حالا»
```

**Right‑to‑left file output:** when it writes a Word/PDF/HTML file, it sets RTL direction, right (leading) alignment, and a Persian‑capable font, so the page looks native, not just "Persian text on a left-aligned page."

---

## What's inside

```
skills/persian/
├── SKILL.md                    # workflow + routing (translate / clean / look up)
├── references/
│   ├── pitfalls.md             # 56-rule machine-Persian catalog + worked EN↔FA examples
│   ├── typography-and-rtl.md   # RTL, ZWNJ, digits, punctuation, file rendering
│   ├── register-guide.md       # choosing/holding register
│   ├── review-lenses.md        # quality-review lenses + verification checklist
│   └── lexicon.md              # idiom + collocation choices
├── scripts/
│   ├── persian_lint.py         # deterministic mechanics linter (stdlib only)
│   ├── lookup.py               # builds a compact terminology brief from the banks
│   └── data/{idioms,glossary}.tsv
└── evals/evals.json            # test cases
```

The scripts are pure Python standard library with no dependencies.

---

## Extending the term banks

`scripts/data/idioms.tsv` and `glossary.tsv` are small, hand-curated seeds (format: `EN <TAB> FA <TAB> note`). Add rows to grow coverage; `lookup.py` surfaces only the entries that appear in a given source text, so the banks can scale without bloating context. See `NOTICE` for open-source banks you can ingest.

---

## Contributing

Issues and PRs are welcome, especially new pitfalls, gold exemplars, and term/idiom rows. Run the linter's built-in checks before submitting.

## License

MIT; see [LICENSE](LICENSE).
