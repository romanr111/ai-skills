# Output Formats

Lead with evidence and decision quality, not a calibrated-looking number.

## Single-skill evaluation

```markdown
## Verdict

**Promise fulfillment:** Supported
**Recommendation:** Install with modifications
**Confidence:** Medium
**Coverage:** 90%
**Capability uplift:** Adequate — Inferred
**Intrinsic score:** 78/100 — B *(secondary summary)*
**Rubric:** 2026-09-v2
**Judge model:** <model-id>

<concise verdict>

### Evidence-bound rubric
| Dimension | Band | Evidence |
|---|---|---|
| Activation & scope | strong | `SKILL.md:...` |
| ... | ... | ... |
| Evidence of effectiveness | insufficient_evidence | No representative evals found |

### Promise-to-proof
| Core promise | Status | Evidence / limitation |
|---|---|---|

### Strongest advantages
- ...

### Weaknesses / red flags
- ...

### Counter-case
**Strongest argument this is overrated:** ...
**Dimensions at risk:** ...
**What would change my mind:** ...

### Capability uplift
State whether uplift is **Probed** or **Inferred**. If Probed, summarize task, baseline, runs, blind-judge status, and material trade-offs.
```

Coverage below 85% must be visually obvious. Do not present a low-coverage score as definitive.

## Comparison / ranking

Start with:

```markdown
| Rank | Skill | Promise | Coverage | Uplift | Intrinsic | Fit | Verdict |
|---:|---|---|---:|---|---:|---:|---|
```

Then explain:
1. decisive evidence for #1 over #2;
2. whether the ordering is robust or a near-tie;
3. unique capability and biggest risk of each;
4. conflicts/redundancy;
5. best stack if relevant.

Do not rank by microscopic score differences. Arithmetic is a secondary summary; pairwise decision-relevant evidence leads.

## Discovery

When discovery is material, briefly report:
- search concepts/query families;
- plausible pool size;
- important eligibility/license exclusions;
- shortlist chosen for Standard evaluation.

## Recommendation vocabulary
- `Install`
- `Install with modifications`
- `Use selectively`
- `Skip`
- `Avoid`

## Evidence language
- `Verified`
- `Supported`
- `Plausible`
- `Author claim`
- `Inference`
- `Unproven`
- `Contradicted`
- `Insufficient evidence`
