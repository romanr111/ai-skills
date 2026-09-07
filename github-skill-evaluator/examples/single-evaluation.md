# Example: Single-skill evaluation

This is an illustrative fictional example. Scores are not claims about a real repository.

## Input

Evaluate `acme-labs/visual-regression-skill` for production frontend visual QA.

## Verdict

**Intrinsic Quality:** 86/100 — A  
**Fit for This Use Case:** 94/100  
**Capability Uplift:** High  
**Evidence Strength:** Moderate  
**Confidence:** Medium  
**Recommendation:** Install

The skill adds a concrete capture → compare → classify → fix → recapture loop across defined responsive viewports, with deterministic screenshot tooling and acceptance criteria. Its main weakness is limited evidence that the workflow reduces escaped visual defects across multiple real projects.

### Score breakdown (abridged)

| Dimension | Score | Key evidence |
|---|---:|---|
| Domain expertise | 9/10 | Defines viewport/state matrix and distinguishes structural from pixel variance. |
| Workflow design | 9/10 | Explicit iterative visual regression loop with stop conditions. |
| Verification | 10/10 | Requires recapture and comparison after every material fix. |
| Reusability | 8/10 | Framework-neutral; browser dependency is documented. |
| Evidence effectiveness | 6/10 | Reproducible examples and tests, but no independent benchmark. |
| Capability uplift | 9/10 | Adds deterministic workflow and criteria beyond generic "check the UI" advice. |

### Strongest advantages
- Objective visual verification instead of subjective self-review.
- Clear ownership boundary: validates visuals; does not redesign them.
- Good progressive disclosure for browser/tool details.

### Weaknesses / red flags
- Author claims production use but provides no measured before/after defect data.
- Screenshot threshold defaults may need calibration per project.

### Evidence quality
**Verified:** skill instructions, scripts, example fixtures, test commands.  
**Author claim:** production adoption.  
**Insufficient evidence:** cross-project defect reduction.
