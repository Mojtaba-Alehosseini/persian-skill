# review-lenses.md — the Phase 3 review team

Run these lenses on the draft. For long or important texts, spawn each as a **parallel subagent**
(one Task per lens) so they review independently and at once; for short texts run them inline.
Give each reviewer the source text, your draft, and the terminology brief from `lookup.py`.

## The lenses

1. **diction-grammar** — word precision + syntax. Does each Persian word carry the source's
   exact weight? Check verb tense consistency, **ezafe**, **«را»** for definite objects,
   noun–adjective agreement, prepositions, natural word order. Flag imprecise or over-generic
   choices and any grammatical error.

2. **fluency-eloquence** — natural rhythm and euphony at the register's level. Does the prose
   flow, or read like a calque? Match dignity to the text (a thriller and a treatise differ).

3. **modern-standards** — living modern Persian. Catch archaic/stilted forms, over-Arabic
   phrasing where natural Persian exists, and needlessly complex structures. Keep the register's
   correct formality without drifting into stiff "museum Persian"; prefer «گریه کردند» over
   bookish «گریستند» unless the register demands otherwise.

4. **back-translation** — the fidelity check. Independently translate the Persian draft back to
   English *without looking at the source first*, then compare. Report every divergence
   (lost / added / shifted meaning, new ambiguity) with severity. Also confirm names, numbers,
   and entities match, and that nothing is dropped or added relative to the source.

5. **oral / read-aloud** — read the draft as if spoken. Flag tongue-twisters, consonant
   clusters, broken cadence, and clauses that don't land on a natural breath.

6. **terminology-compliance** — enforce the brief: every glossary and idiom entry from
   `lookup.py` is used consistently and correctly.

## Conflict-resolution priority (when lenses disagree)
1. Meaning fidelity (back-translation) — highest
2. Terminology compliance
3. Grammatical correctness
4. Oral fluency
5. Register & style
6. Modern accessibility
7. Aesthetic preference — lowest

## Output discipline
Show the user only the final translation + a 2–3 sentence summary. Never dump drafts, individual
lens reports, or the back-translation unless they ask.

## Verification checklist (Phase 4–5, before delivering)
Confirm two things on every real translation:

1. **Completeness & accuracy.** Render the full meaning of the source. Don't omit, add, or soften
   content; preserve the author's tone and intent.
2. **Verify against the source.** Re-check every: proper noun / name (spelling, transliteration,
   identity); place name & geography; number, date, age, quantity; unit conversion (recompute and
   apply the user's unit policy consistently); polarity / quantifier (easy to flip — "no one" vs
   "everyone", "missing" vs "present").

The **back-translation** lens above is the fastest way to catch a shifted or dropped meaning:
translate the Persian back to English independently, then compare.
