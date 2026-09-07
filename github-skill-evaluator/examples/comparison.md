# Example: comparison without false precision

Fictional example; not benchmark evidence.

## Ranking

| Rank | Skill | Promise | Coverage | Uplift | Intrinsic | Fit | Verdict |
|---:|---|---|---:|---|---:|---:|---|
| 1 | Skill A | Supported | 95% | Strong — Probed | 82 | 93 | Install |
| 2 | Skill B | Partially supported | 90% | Adequate — Inferred | 79 | 88 | Install with modifications |
| 3 | Skill C | Unproven | 80% | Weak — Inferred | 67 | 72 | Use selectively |

Skill A wins because it has a concrete workflow plus a same-model baseline probe showing material improvement on the requested task. Skill B is close in secondary arithmetic but lacks probe evidence, so the three-point score gap is not the reason for the ordering. Skill C is portable and polished but largely restates generic advice.

### Decisive evidence

- **A:** representative probe + explicit verification loop.
- **B:** strong static methodology, but uplift remains inferred.
- **C:** documentation is stronger than behavioral evidence.

### Stack compatibility

A + a dedicated visual-QA skill may be complementary if responsibilities are separated. A + B likely duplicates design-generation guidance and increases instruction conflict/context cost.

### Counter-cases

For each candidate, record the strongest argument against its placement and what observation would change the ranking. Do not hide disagreement behind decimal scores.
