# Output Formats

## Discovery + ranking

When the user asks you to **find** candidates, start with the decision rather than a search-log dump.

```markdown
## Ranking

| Rank | Skill | Intrinsic | Fit | Promise fulfillment | Uplift | Evidence | Verdict |
|---:|---|---:|---:|---|---|---|---|
| 1 | ... | 88 | 94 | Supported | High | Moderate | Install |
| 2 | ... | 84 | 81 | Partially supported | Moderate | Moderate | Use selectively |
```

Then briefly state:
- candidate pool/shortlist size when useful;
- material eligibility exclusions such as unclear license or incompatible tooling;
- why #1 wins;
- whether the gap is meaningful or within uncertainty;
- which important promises were actually supported versus unproven.

Do not list every search result unless requested.

## Single-skill evaluation

```markdown
## Verdict

**Intrinsic Quality:** 84/100 — A
**Fit for This Use Case:** 91/100
**Promise Fulfillment:** Supported
**Capability Uplift:** High
**Evidence Strength:** Moderate
**Confidence:** Medium
**Recommendation:** Install with modifications

<one concise paragraph explaining the decision>

### Promise-to-proof

| Core promise | Status | Best evidence | Limitation |
|---|---|---|---|
| ... | Supported | ... | ... |
| ... | Unproven | ... | ... |

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
<what was directly verified, what repository evidence supports, what is author claim, and what remains unvalidated>
```

Omit `Fit for This Use Case` when the user provides no use case. Keep the promise table to material/core claims; omit trivial claims.

## Comparison / ranking when candidates were supplied

Start with:

```markdown
| Rank | Skill | Intrinsic | Fit | Promise fulfillment | Uplift | Evidence | Verdict |
|---:|---|---:|---:|---|---|---|---|
| 1 | ... | 88 | 94 | Supported | High | Moderate | Install |
| 2 | ... | 84 | 81 | Unproven | Moderate | Weak | Install selectively |
```

Then explain:
1. why #1 wins;
2. whether the difference is meaningful or within uncertainty;
3. unique capability of each candidate;
4. which central claims are verified/supported/unproven/contradicted;
5. biggest weakness/risk of each;
6. redundancies and conflicts;
7. best stack, if relevant.

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

## Promise fulfillment vocabulary

Use one overall label when material:
- `Verified`
- `Supported`
- `Partially supported`
- `Unproven`
- `Contradicted`

For individual claims, `Plausible` and `Not testable here` may also be useful. Do not use `Verified` unless the relevant behavior/claim was directly reproduced or independently confirmed.

## Evidence language

Prefer precise labels when they clarify uncertainty:
- **Verified:** directly inspected and executed/reproduced for the claim at issue.
- **Repository evidence / Supported:** source/tests/config meaningfully support it but were not independently reproduced.
- **Author claim:** stated but not independently supported.
- **Inference / Plausible:** reasoned from available evidence.
- **Unproven / Insufficient evidence:** conclusion cannot be supported.
- **Contradicted:** observed evidence conflicts with the claim.

## Recommendation vocabulary

Use one:
- `Install`
- `Install with modifications`
- `Use selectively`
- `Skip`
- `Avoid`

Tie the recommendation to expected capability uplift, promise evidence, integration cost, and risk.
