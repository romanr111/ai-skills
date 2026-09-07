# Output Formats

## Single-skill evaluation

```markdown
## Verdict

**Intrinsic Quality:** 84/100 — A
**Fit for This Use Case:** 91/100
**Capability Uplift:** High
**Evidence Strength:** Moderate
**Confidence:** Medium
**Recommendation:** Install with modifications

<one concise paragraph explaining the decision>

### Score breakdown

| Dimension | Score | Key evidence |
|---|---:|---|
| Problem definition and scope | 8/10 | ... |
| Instruction quality | 9/10 | ... |
| ... | ... | ... |

### Strongest advantages
- ...

### Weaknesses / red flags
- ...

### Capability uplift
<what the agent gains versus a strong frontier model without the skill>

### Evidence quality
<what is verified, what is author claim, and what remains unvalidated>
```

Omit `Fit for This Use Case` when the user provides no use case.

## Comparison / ranking

Start with:

```markdown
| Rank | Skill | Intrinsic | Fit | Uplift | Evidence | Verdict |
|---:|---|---:|---:|---|---|---|
| 1 | ... | 88 | 94 | High | Moderate | Install |
| 2 | ... | 84 | 81 | Moderate | Strong | Install selectively |
```

Then explain:
1. why #1 wins;
2. whether the difference is meaningful or within uncertainty;
3. unique capability of each candidate;
4. biggest weakness/risk of each;
5. redundancies and conflicts;
6. best stack, if relevant.

## Stack analysis

```markdown
### Recommended stack

1. **Skill A** — owns <responsibility>.
2. **Skill B** — owns <responsibility>.

**Complementarity:** ...
**Overlap:** ...
**Instruction conflicts:** ...
**Context cost:** ...
**Activation order:** ...
```

Do not recommend a stack merely because its members have the highest individual scores.

## Evidence language

Prefer precise labels when they clarify uncertainty:
- **Verified:** directly inspected/executed.
- **Repository evidence:** supported by source/tests/config.
- **Author claim:** stated but not independently supported.
- **Inference:** reasoned from available evidence.
- **Insufficient evidence:** conclusion cannot be supported.

## Recommendation vocabulary

Use one:
- `Install`
- `Install with modifications`
- `Use selectively`
- `Skip`
- `Avoid`

Tie the recommendation to both expected capability uplift and integration/risk cost.
