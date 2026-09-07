# review-lenses.md: the Phase 3 review, and the verification checklist

Run these lenses on the draft. If you can spawn subagents (Claude Code, Cowork), run one per lens
in parallel for long or important texts. Otherwise run them inline, one after another, in the
order below. Give each reviewer the source, the draft, and the terminology brief from `lookup.py`.

## The lenses

1. **back-translation (fidelity).** Translate the Persian draft back to English without looking at
   the source first, then compare. Report every divergence (lost, added, shifted meaning, new
   ambiguity) with severity. Confirm names, numbers, dates, and entities match, and that nothing was
   dropped, added, or softened. This lens has the final say.

2. **terminology-compliance.** Every glossary and idiom entry from `lookup.py` is used consistently
   and correctly.

3. **diction-grammar.** Word precision and syntax. Does each Persian word carry the source's exact
   weight? Check verb tense consistency, ezafe, «را» for definite objects, prepositions, natural
   word order. Flag imprecise or over-generic choices and any grammatical error.

4. **ai-tells.** Read `ai-tells.md`. Flag bureaucratic verbs (می‌باشد، مورد … قرار گرفتن، توسط),
   calqued «یک» and «به عنوان», filler and announcements, rule-of-three, piled connectors, em
   dashes, and uniform sentence rhythm. Also the machine-Persian tells from `pitfalls.md`:
   calqued passives (P32), it-clefts (P1), flat dialogue (P8).

5. **fluency-eloquence.** Natural rhythm at the register's level. Does the prose flow, or read like
   a calque? Match dignity to the text; a thriller and a treatise differ.

6. **modern-standards.** Living modern Persian. Catch archaic or stilted forms, over-Arabic phrasing
   where natural Persian exists, needlessly complex structure. Keep the register's formality without
   drifting into "museum Persian": «گریه کردند» over «گریستند» unless the register demands it.

7. **oral / read-aloud.** Read the draft as if spoken. Flag tongue-twisters, consonant clusters,
   broken cadence, and clauses that don't land on a natural breath.

## Conflict-resolution priority (when lenses disagree)
1. Meaning fidelity (back-translation): highest
2. Terminology compliance
3. Grammatical correctness
4. No AI tells
5. Oral fluency
6. Register and style
7. Modern accessibility
8. Aesthetic preference: lowest

## Output discipline
Show the user only the final translation plus a two- or three-sentence note on the choices that
matter. Never dump drafts, lens reports, or the back-translation unless asked.

## Verification checklist (before delivering)
Confirm on every real translation:

1. **Complete and faithful.** The full meaning of the source is rendered. Nothing omitted, added, or
   softened. Alcohol, sex, politics, and religion are translated as written; published Iranian
   editions cut these, and a model trained on them may too. You don't. The author's tone and intent
   survive.
2. **Checked against the source.** Every proper noun (spelling, transliteration, identity), place
   name, number, date, age, quantity, unit conversion (recomputed, and consistent with the user's
   unit policy), and every polarity or quantifier ("no one" vs "everyone", "missing" vs "present").
3. **Mechanically clean.** `persian_lint.py --fix` has run, or sections 1 to 4 of
   `typography-and-rtl.md` were applied by hand.

The back-translation lens is the fastest way to catch a shifted or dropped meaning.
