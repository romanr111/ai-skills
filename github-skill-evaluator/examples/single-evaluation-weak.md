# Example: polished but weakly evidenced skill

Fictional example; not benchmark evidence.

## Verdict

**Promise fulfillment:** Unproven
**Recommendation:** Skip
**Confidence:** Medium
**Coverage:** 90%
**Capability uplift:** Weak — Inferred
**Intrinsic score:** 36/100 — F *(secondary summary)*
**Rubric:** 2026-09-v2
**Judge model:** example-model

The repository is polished, but most behavioral guidance is generic and its headline quality claims are unsupported by representative tests or baseline comparisons.

### Evidence-bound rubric

| Dimension | Band | Evidence |
|---|---|---|
| Activation & scope | adequate | broad but usable description |
| Instruction & workflow | weak | generic checklist with little branching |
| Domain expertise | weak | mostly common best practices |
| Verification | weak | self-review language without observable acceptance criteria |
| Capability uplift | weak | no unique procedure/tooling beyond baseline behavior |
| Evidence of effectiveness | insufficient_evidence | screenshots and README claims only |
| Safety | adequate | no destructive behavior, but safeguards are sparse |
| Reusability & composability | adequate | portable format, limited integration guidance |
| Context efficiency | weak | large monolithic SKILL.md with duplicated prose |
| Maintainability & docs | strong | clear install docs and license |

The 36/100 secondary score is the deterministic result of the bands above after the 10% Evidence-of-effectiveness weight abstains and the remaining 90% renormalizes.

### Counter-case

**Strongest argument this is underrated:** even generic reminders can improve consistency for weaker models or inexperienced users.

**Dimensions at risk:** Capability uplift, Instruction & workflow.

**What would change my mind:** a same-model baseline probe showing materially better task outcomes with the skill enabled.
