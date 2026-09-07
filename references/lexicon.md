# lexicon.md: idiom, term, and collocation choices

Idioms and collocations are where literal translation fails hardest, and the right term depends on
the collocation (the dictionary's first hit is often the machine-Persian tell). Don't load the whole
banks; run the lookup so only the entries in *your* text surface:

    python scripts/lookup.py <source_file>

Full banks: `scripts/data/idioms.tsv` and `scripts/data/glossary.tsv` (seed sets; extend them, see
`NOTICE`). Rule: translate the function, not the words. An English idiom maps to a Persian idiom or
a recast clause, never a calque.

## High-value idiom patterns
- to my name → «دار و ندار»: «همهٔ دار و ندارم ده دلار بود» (P37)
- establish ourselves / make it → «به جایی رسیدن» (not «خود را تثبیت کردن») (P40)
- my turn came → «نوبت به من رسید» (P42)
- on a budget → «حواسم به خرجم بود» / «با پول کم» (P44)
- perfect timing → «چه به‌موقع!»; how about …? → «موافقی…؟ / چطوره…؟» (P13)
- lose your temper → «از کوره در رفتن»; out of the blue → «یک‌دفعه / بی‌مقدمه»
- a blessing in disguise → «توفیق اجباری»; the last straw → «کاسهٔ صبر را لبریز کردن»
- bite the bullet → «دندان روی جگر گذاشتن» (endure); take the plunge → «دل به دریا زدن» (risk).
  These two are often confused.
- under the weather → «ناخوش بودن» (physically unwell; «دمغ» means sulky)
- no pain, no gain → «نابرده رنج گنج میسر نمی‌شود» (Saadi; the standard equivalent)
- speak of the devil → «حلال‌زاده است»

## Collocation reminders
- business partner → «شریک تجاری» (not «شریک کاری»); business (topic) → «کسب‌وکار» (not «تجارت») (P4/P7)
- smoking room → «اتاق دخانیات» (not «اتاق سیگار») (P7)
- the lights went out → «برق رفت» (not «چراغ‌ها خاموش شد») (P12)
- grim (mood) → «گرفته» (not «عبوس») (P4)
- comic books → «کتاب کمیک / مصور»; «کمیک» is established, «طنز» is wrong (P33)
- recital → «شعرخوانی» for poetry, «رسیتال / اجرا» for music (P14)
- artichoke → «کنگر فرنگی»; plum → «آلو»; «آلوچه» is the small sour plum (P23)
- artificial intelligence / AI → «هوش مصنوعی» (the Persian Academy's term and the common one)
- omen → «نشانه / فال»; bad omen → «بدشگون / بدیمن»

## Domestication with care (P23)
Localize where it helps, but don't lose needed specificity: yams → «سیب‌زمینی» drops the meaning.
When it matters, keep the term and footnote it.

## Never soften
Published Iranian translations often cut or blur alcohol, pork, sex, and politics, and a model that
learned from them may do the same. Translate as written: wine → «شراب», got drunk → «مست شد»,
pork → «گوشت خوک», bacon → «بیکن». If the user wants a sanitized version, they will ask.

## House-style coinages (opt-in only)
These are the author's own coinages. They are **not** the default. Use them only when the user asks
for "house style" or names one. Where they would read more foreign than the standard word, the
modern-standards lens wins.

| EN | Default (use this) | House-style coinage (opt-in) |
|---|---|---|
| artificial intelligence / AI | «هوش مصنوعی» | «هوشواره» |
| quote (a quotation) | «نقل‌قول» | «گفتاورد» (accepted neologism, still rarer) |
| transportation | «حمل‌ونقل» | «ترابری» (the official term; fine in formal text) |
| manipulator | «اهل دستکاری روانی / فریبکار» | «روان‌دستکاری» |
| sugarcoat | «لاپوشانی / شیرین جلوه دادن» | «شکرپیچ» |
| lifestyle | «سبک زندگی» | «زیست‌شیوه» |
| Christian | «مسیحی» | «عیسوی» (archaic) |
| context | «بافت / زمینه» | «بافتار» (linguistics register) |
| impression | «برداشت / تأثیر» | avoid the loan «انطباع» in modern prose |

Accepted neologisms that are fine as defaults: «تراکنش» (transaction), «تراجنسیتی» (transgender).
For concepts with no standard equivalent, a coinage is the best available choice: «شبه‌رابطه»
(situationship), «هوش‌محرک» (sapiosexual).
