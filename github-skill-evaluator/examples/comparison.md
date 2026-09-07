# Example: Comparison and stack selection

Illustrative fictional repositories.

| Rank | Skill | Intrinsic | Fit: premium web implementation | Uplift | Evidence | Verdict |
|---:|---|---:|---:|---|---|---|
| 1 | `precision-ui/frontend-craft` | 88 | 93 | High | Moderate | Install |
| 2 | `pixelsafe/visual-qa` | 86 | 91 | High | Strong | Install |
| 3 | `viral-prompts/beautiful-ui` | 67 | 73 | Low | Weak | Use selectively |

## Why #1 wins

`frontend-craft` encodes stronger generation-time design decisions: hierarchy, typography, responsive structure, component constraints, and implementation checks. `visual-qa` is slightly stronger in evidence and verification but is primarily an evaluator, not a generator. The score difference is small enough that the two should be considered peers for different responsibilities rather than substitutes.

## Best combination

1. **frontend-craft** — owns design/implementation decisions.
2. **visual-qa** — owns independent capture/comparison and regression verification.

**Complementarity:** High. Generation and verification are distinct.  
**Overlap:** Both mention responsive/accessibility checks, but ownership remains separable.  
**Instruction conflicts:** None material found.  
**Context cost:** Moderate; load visual QA after implementation or at explicit validation gates.  
**Activation order:** frontend-craft → visual-qa → targeted frontend-craft fixes → visual-qa recheck.

Do not add `beautiful-ui` by default: it overlaps with generation guidance while adding little unique capability, increasing context cost and instruction ambiguity.
