# Example: Popular but weak skill

This is an illustrative fictional example.

## Input

Evaluate `popular-dev/ultimate-clean-code-skill`, a repository with 18k GitHub stars.

## Verdict

**Intrinsic Quality:** 52/100 — D  
**Capability Uplift:** Low  
**Evidence Strength:** Weak  
**Confidence:** High  
**Recommendation:** Skip

The repository is polished and popular, but most instructions restate generic software-engineering principles. It lacks a concrete review procedure, failure taxonomy, verification loop, and evidence that installing the skill improves a strong model's output.

### Decisive evidence
- `SKILL.md` repeatedly says to use SOLID, clean naming, tests, and best practices without decision rules.
- No eval suite or before/after comparison was found.
- Examples show only successful greenfield code and do not exercise trade-offs or failure cases.
- GitHub popularity is recorded under Community evidence only and contributes little to the total.

### Capability uplift
Low: a strong model already follows most of the instructions reliably. The skill provides reminders rather than unique procedures or knowledge.
