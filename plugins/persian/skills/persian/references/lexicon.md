# lexicon.md — idiom, term & collocation choices

Idioms and collocations are where literal translation fails hardest, and the right term is
collocation-dependent (the dictionary's first hit is often the machine-Persian tell). Don't load the
whole banks — run the lookup so only the entries in *your* text surface:

    python scripts/lookup.py <source_file>

Full banks: `scripts/data/idioms.tsv` and `scripts/data/glossary.tsv` (seed; extend — see `NOTICE`).
Rule: translate the **function, not the words** — an English idiom maps to a Persian idiom or a
recast clause, never a calque.

## High-value idiom patterns
- to my name → anchor to a concrete noun: «حسابی بانکی معادلِ ده دلار» (not «ده دلار پول») — P37
- establish ourselves / make it → «به جایی رسیدن» (not «خود را تثبیت کردن») — P40
- my turn came → «نوبت به من رسید» — P42
- on a budget → «حواسم بود چقدر خرج می‌کنم» — P44
- perfect timing → «چه به‌موقع!»; how about …? → «موافقی…؟ / چطوره…؟» — P13
- lose your temper → «از کوره در رفتن»; out of the blue → «یک‌دفعه / بی‌مقدمه»
- a blessing in disguise → «توفیقِ اجباری»; the last straw → «کاسهٔ صبر را لبریز کردن»

## Collocation reminders
- business partner → «شریکِ تجاری» (not «شریکِ کاری»); business (topic) → «کسب‌وکار» (not «تجارت») — P4/P7
- smoking room → «اتاقِ دخانیات» (not «اتاقِ سیگار») — P7
- the lights went out → «برق رفت» (not «چراغ‌ها خاموش شد») — P12
- grim (mood) → «گرفته» (not «عبوس») — P4
- comic books → «کتاب‌های مصور» (not «کمیک‌بوک») — P33
- recital → «شعرخوانی»; graduate dormitory → «خوابگاهِ دانشجویانِ فوق‌لیسانس و دکترا» — P14/P33
- artificial intelligence / AI → «هوشواره» (preferred term; common alternative «هوش مصنوعی»)

## Domestication with care (P23)
Localize where it helps (artichokes → «کنگر»), but don't lose needed specificity (yams →
«سیب‌زمینی» drops the meaning); when it matters, keep the term and footnote it.

## House-style preferences (optional — not the default)
These are preference choices. Where a row sets a specific default, use it. For the rest, prefer the
standard term unless the user asks otherwise, and avoid any coinage that would read *more* foreign than
the word it replaces.

| EN | Default — use this | House-style coinage |
|---|---|---|
| Christian | «مسیحی» | «عیسوی» (archaic) |
| impression | «برداشت / تأثیر» | — «انطباع» is a loan; avoid in modern prose |
| manipulator | «اهلِ دستکاریِ روانی» | «روان‌دستکاری» |
| sugarcoat | «لاپوشانی» | «شکرپیچ» |
| insecure (emotion) | «نامطمئن / دل‌نگران» | «متزلزل» = "unstable" (weaker fit) |
| lifestyle | «سبکِ زندگی» | «زیست‌شیوه» |
| context | «بافت / زمینه» | «بافتار» (linguistics register) |

Accepted neologisms that are fine as defaults: «گفتاورد» (quote), «ترابری» (transportation),
«تراکنش» (transaction), «تراجنسیتی» (transgender). For concepts with no standard equivalent —
«شِبهِ رابطه» (situationship), «هوش‌محرک» (sapiosexual) — the coinage is the best available choice.
