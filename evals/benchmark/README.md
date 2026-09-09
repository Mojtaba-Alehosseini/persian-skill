# Raw benchmark data

Everything behind [`../BENCHMARK.md`](../BENCHMARK.md). Four files, so the numbers can be
recounted or disputed without rerunning anything.

| file | contents |
|---|---|
| `prompts.json` | the 11 evals as given: route, the exact user request, the assertions |
| `outputs.json` | every generated answer, keyed `eval → condition_run`. `skill_r1` = with the skill, first run; `base_r2` = without it, second run. Evals 1, 5, 8, 9, 10, 11 have three runs per condition; the rest have one. |
| `verdicts.json` | grader output. `run1` is keyed by the anonymised labels A/B, `run2` by candidate position 1–6. |
| `key.json` | which anonymised label was which condition. The graders never saw this. |

## Recounting the totals

```python
import json
v = json.load(open("verdicts.json")); k = json.load(open("key.json"))
agg = {"skill": [0, 0], "base": [0, 0]}
for ev, slots in v["run2"].items():
    for pos, arm in enumerate(k["run2_candidate_order"][ev], start=1):
        res = slots[str(pos)]
        agg[arm][0] += sum(x["verdict"].upper().startswith("PASS") for x in res)
        agg[arm][1] += len(res)
print(agg)   # {'skill': [61, 63], 'base': [51, 63]}
```

## Rerunning it

Two conditions, same model, one variable.

- **without the skill** — give an agent only the text of one `prompt`, and tell it to read no
  other file. One fresh agent per eval, so no eval primes another.
- **with the skill** — give an agent the same prompt, plus: read `SKILL.md`, follow its routing
  table into `references/`, run its scripts.
- **grading** — hand a separate model the request, the assertions, and the outputs shuffled and
  anonymised. Strict PASS/FAIL per assertion, partial credit counts as FAIL. Read `key.json`
  only after grading.
