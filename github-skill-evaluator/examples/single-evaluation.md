# Example: strong skill with incomplete effectiveness evidence

Fictional example showing the output shape; it is not benchmark evidence.

## Verdict

**Promise fulfillment:** Supported
**Recommendation:** Install
**Confidence:** Medium
**Coverage:** 90%
**Capability uplift:** Adequate — Inferred
**Intrinsic score:** 79/100 — B *(secondary summary)*
**Rubric:** 2026-09-v2
**Judge model:** example-model

The skill has a strong operational workflow, clear activation boundaries, and concrete verification loops. Its main limitation is empirical: no matched baseline probe or representative repeated eval demonstrates incremental model uplift, so uplift remains Inferred rather than Probed.

### Evidence-bound rubric

| Dimension | Band | Evidence |
|---|---|---|
| Activation & scope | strong | `SKILL.md:12-30` explicit trigger/non-goals |
| Instruction & workflow | strong | `SKILL.md:34-91` staged procedure |
| Domain expertise | strong | `references/method.md:10-55` specialist failure modes |
| Verification | strong | `SKILL.md:96-120` fix/recheck loop |
| Capability uplift | adequate | no baseline probe; inferred from concrete workflow |
| Evidence of effectiveness | insufficient_evidence | no representative comparative eval found |
| Safety | strong | `SKILL.md:124-145` scoped non-destructive behavior |
| Reusability & composability | strong | portable paths and explicit dependencies |
| Context efficiency | strong | compact SKILL.md + on-demand references |
| Maintainability & docs | strong | clear installation/license/version notes |

### Counter-case

**Strongest argument this is overrated:** a current frontier model may already perform most of the workflow when directly prompted, so the skill may mainly improve consistency rather than capability.

**Dimensions at risk:** Capability uplift, Instruction & workflow.

**What would change my mind:** a matched blind baseline probe showing equivalent outputs across several representative tasks.
