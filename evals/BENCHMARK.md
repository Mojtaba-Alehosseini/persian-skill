# Benchmark: does the skill actually change the output?

A skill is only worth installing if the same model does measurably better with it than
without it. This file is the measurement, the method, and the raw data, so you can
disagree with any of it.

## Result

**Run 1 — all 11 evals, one sample each**

| | assertions passed |
|---|---|
| Claude Sonnet **with** the skill | **40 / 40 (100%)** |
| Claude Sonnet **without** the skill | 32 / 40 (80%) |

One sample per condition is not enough to trust, because the baseline is not
consistently wrong — it is *sometimes* right. So the six evals where the baseline
failed at least one assertion were re-run three times per condition:

**Run 2 — the 6 discriminating evals, 3 samples each condition**

| eval | task | with skill | without |
|---|---|---|---|
| 1 | EN→FA literary memoir | 12/12 | 11/12 |
| 5 | idiom lookup | 5/6 | 3/6 |
| 8 | mixed FA+EN typography | 15/15 | 13/15 |
| 9 | unit policy (must ask) | 8/9 | 7/9 |
| 10 | de-AI a Persian paragraph | 12/12 | 10/12 |
| 11 | passive → impersonal active; «چرا» | 9/9 | 7/9 |
| | **total** | **61/63 (97%)** | **51/63 (81%)** |

The honest headline is **97% vs 81%**, not 100%. The skill missed twice, both times on
a user-facing protocol rule rather than on Persian quality: once it gave idiom options
without explicitly warning against the literal rendering, and once it translated a
measurement instead of asking about the unit policy first.

## What the gap is actually made of

The baseline is good at mechanics. Modern Claude already gets ZWNJ, ی/ک and Persian
digits right most of the time — on the pure-mechanics evals (4, 7) the two conditions
produced **byte-identical** Persian. If this skill were only a typography fixer, the
benchmark would show nothing.

Every point of the gap came from four places:

1. **Idioms, not paraphrase.** *"ten dollars to my name"* → «همهٔ دار و ندارم … ده دلار بود».
   The baseline reached for «تنها دارایی‌ام» or the calque «تمام دارایی‌ای که به نام من بود».
2. **Idiom accuracy.** Asked for the Persian for *"cost an arm and a leg"*, the baseline in
   one run recommended «به قیمت خون پدرم تمام شد» and asserted it is "used all the time".
   It is not an established idiom for expense. Confident invention is worse than no answer.
3. **Grammar Persian has and English does not.** *"Isn't that the day…?" — "Yes."* is
   «چرا، هست», never «بله». The baseline answered «بله» in 2 of 3 runs.
4. **Not touching what wasn't asked.** In a mixed Persian/English text, the baseline
   "fixed" the English straight quotes into curly ones in 2 of 3 runs. The instruction was
   to clean the Persian.

## Method

- **Model:** Claude Sonnet, identical in both conditions. Only the skill differs.
- **Prompts:** the 11 evals in [`evals.json`](evals.json), unchanged, one per fresh agent
  with no shared context, so no eval primes another.
- **With-skill condition:** the agent is told to read `SKILL.md`, follow its routing table
  into `references/`, and run the scripts. Nothing else.
- **Without-skill condition:** the agent gets the user request and nothing else, and is
  told not to read any other file.
- **Grading:** every eval's assertions were pre-written in `evals.json` *before* this
  benchmark existed. A separate Claude Opus grader saw the request, the assertions, and
  the anonymised outputs in shuffled order, with no indication of which condition produced
  which. Partial satisfaction counts as a fail.
- **Mechanics cross-check:** `persian_lint.py --check --style` was run over all outputs as
  a deterministic second opinion. It reported both conditions clean, which is the point
  made above.
- **Raw data:** every prompt, every output, and every grader verdict is in
  [`benchmark/`](benchmark/).

## What this does not show

- One model (Sonnet) on one day. Opus baselines are stronger; the gap will be smaller.
- 11 evals, 40 assertions. Small. Treat the per-eval rows as illustrations, not statistics.
- The evals were written by the skill's author. They encode what this skill thinks matters
  — Persian idiom, fidelity, register, unit policy. A different author would test different
  things and get a different number.
- An LLM graded the craft assertions. The mechanics assertions were verified at codepoint
  level; the craft ones rest on the grader's Persian.

## Reproducing it

Everything needed is in `benchmark/`: `prompts/` (one file per eval), `outputs/`
(both conditions, all runs), `verdicts/` (grader JSON), and `key.json` (which anonymised
candidate came from which condition — read it after grading, not before).
