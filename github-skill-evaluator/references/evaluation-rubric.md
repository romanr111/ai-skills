# Evaluation Rubric

## Table of contents

1. Scoring rules
2. Weights
3. Dimension anchors
4. Overall tier calibration
5. Evidence and uncertainty

## 1. Scoring rules

Score each dimension from 0–10.

General anchors:
- **0–1**: absent, broken, unsafe, or actively harmful.
- **2–3**: major deficiencies; little reusable value.
- **4–5**: partial/basic implementation with notable weaknesses.
- **6–7**: solid and useful; meaningful limitations remain.
- **8–9**: strong/expert implementation with minor limitations.
- **10**: exceptional and unusually complete; reserve for rare cases.

Use 0.5 increments when helpful. Avoid pseudo-precision beyond that.

## 2. Weights

| # | Dimension | Weight |
|---:|---|---:|
| 1 | Problem definition and scope | 4% |
| 2 | Instruction quality | 7% |
| 3 | Domain expertise | 8% |
| 4 | Workflow design | 8% |
| 5 | Verification and self-correction | 9% |
| 6 | Reusability | 8% |
| 7 | Composability | 4% |
| 8 | Context efficiency | 4% |
| 9 | Tool usage | 3% |
| 10 | Code/script quality | 3% |
| 11 | Evidence of effectiveness | 8% |
| 12 | Maintainability | 5% |
| 13 | Safety and failure modes | 8% |
| 14 | Model leverage / capability uplift | 9% |
| 15 | Engineering/design sophistication | 5% |
| 16 | Documentation quality | 4% |
| 17 | Repository health | 2% |
| 18 | Community evidence | 1% |
|  | **Total** | **100%** |

Popularity is intentionally capped at 1% through Community evidence. Repository health is also secondary.

Normalized score:

`overall = Σ(dimension_score / 10 × weight)`

## 3. Dimension anchors

### 1. Problem definition and scope — 4%

Assess purpose, meaningful use case, activation boundaries, non-goals, and appropriate specialization.

High score:
- clear problem and trigger;
- explicit or inferable non-goals;
- scope is narrow enough to execute but broad enough to be useful.

Low score:
- vague "improve everything" positioning;
- unclear trigger;
- uncontrolled scope creep.

### 2. Instruction quality — 7%

Assess clarity, specificity, ordering, decision rules, edge cases, failure handling, contradictions, and model-friendly structure.

High score: instructions materially constrain and improve execution.
Low score: generic prose, slogans, ambiguous sequencing, contradictions.

### 3. Domain expertise — 8%

Assess non-obvious heuristics, standards, specialist decision criteria, trade-offs, failure modes, terminology, and expert constraints.

High score: encodes knowledge/procedure a general model would not reliably reconstruct on every run.
Low score: restates common best practices.

### 4. Workflow design — 8%

Assess executable sequencing, branches, inspection-before-action, stop criteria, evidence collection, iteration, escalation, and output contract.

High score: turns expertise into a reliable procedure.
Low score: describes goals without an operational path.

### 5. Verification and self-correction — 9%

Assess tests, assertions, validation, independent checks, acceptance criteria, visual/reference comparison, adversarial review, and explicit definition of done.

High score: verification is first-class and tied to likely failure modes.
Low score: "generate and trust" workflow or vague self-check language with no observable criteria.

### 6. Reusability — 8%

Assess portability across repositories, organizations, stacks, providers, and operating systems where relevant. Identify hidden assumptions.

Penalize unjustified coupling to private infrastructure, absolute paths, undocumented environment variables, or one repository convention.

Do not penalize legitimate domain specialization.

### 7. Composability — 4%

Assess clear boundaries, predictable inputs/outputs, delegation, overlap, activation conflicts, and ability to coexist with other skills.

High score: responsibility is distinct and integration points are clear.
Low score: tries to orchestrate unrelated domains or overrides other skills unpredictably.

### 8. Context efficiency — 4%

Assess information density, progressive disclosure, duplicate instructions, unnecessary examples, and token cost versus behavioral benefit.

High score: concise entry point with references loaded only when needed.
Low score: prompt bloat, duplicated philosophy, giant monolithic skill.

### 9. Tool usage — 3%

If tools are relevant, assess necessity, clear invocation conditions, error handling, portability, deterministic automation, and security.

If tools are not needed, a well-designed tool-free skill can score highly.

### 10. Code/script quality — 3%

When scripts exist, assess correctness, simplicity, dependencies, maintainability, error handling, idempotency, safety, and tests.

When scripts are unnecessary and intentionally omitted, score based on appropriateness rather than absence.

### 11. Evidence of effectiveness — 8%

Evidence hierarchy:
- **9–10**: strong repeatable evals/benchmarks, measured outcomes, independent validation.
- **7–8**: meaningful tests plus realistic repeated examples or real-world evidence.
- **5–6**: reproducible examples but limited comparative/effectiveness evidence.
- **3–4**: mostly author claims, screenshots, usage anecdotes.
- **0–2**: no evidence or evidence contradicts claims.

Do not convert stars into effectiveness evidence.

### 12. Maintainability — 5%

Assess structure, modularity, naming, stable interfaces, versioning where useful, dependency risk, and complexity proportionality.

Recent commits are not required for a mature stable skill.

### 13. Safety and failure modes — 8%

Assess destructive commands, permissions, secrets, remote execution, supply-chain exposure, hallucination-sensitive operations, uncontrolled modifications, silent failure, confirmations, and rollback/recovery.

A severe uncontrolled safety defect may cap the final tier regardless of arithmetic.

### 14. Model leverage / capability uplift — 9%

Compare against a strong current frontier model without the skill.

High score requires concrete incremental value such as:
- specialist procedures;
- reliable deterministic tooling;
- domain-specific constraints;
- validation loops;
- non-obvious decision frameworks;
- integration knowledge;
- repeatable context unavailable from the base model.

Generic instructions such as "write clean code", "use best practices", or "think carefully" score low.

Suggested mapping:
- 9–10 Transformative
- 8 High
- 5–7 Moderate
- 2–4 Low
- 0–1 Negligible

### 15. Engineering/design sophistication — 5%

Assess systems thinking, abstraction boundaries, feedback loops, useful heuristics, trade-off handling, and proportionality.

Do not equate sophistication with more files, more patterns, or more abstractions.

### 16. Documentation quality — 4%

Assess setup, examples, inputs, outputs, dependencies, limitations, troubleshooting, and discoverability.

Documentation supports usability but cannot compensate for shallow methodology.

### 17. Repository health — 2%

Assess maintenance risk, unresolved critical defects, releases, contributor concentration where material, and dependency freshness.

Treat stable low-activity repositories fairly.

### 18. Community evidence — 1%

Consider stars, forks, watchers, contributors, discussions, external mentions, and independent usage only as weak supporting signals.

Never infer intrinsic quality from popularity.

## 4. Overall tier calibration

| Tier | Score | Meaning |
|---|---:|---|
| S | 90–100 | Exceptional; unusually strong methodology, implementation, evidence, reusability, and uplift. |
| A | 80–89 | Strong production-quality skill with identifiable limitations. |
| B | 70–79 | Useful; meaningful incompleteness, narrowness, weak validation, or redundancy remains. |
| C | 55–69 | Some useful ideas but significant weaknesses or limited reuse value. |
| D | 40–54 | Low-value implementation or substantial problems. |
| F | <40 | Poor, misleading, unsafe, broken, or essentially useless. |

Arithmetic is a starting point. Apply severe safety/integrity caps from `red-flags.md`.

## 5. Evidence and uncertainty

For each material claim, label internally or explicitly as appropriate:
- **Verified** — directly observed or executed.
- **Supported by repository evidence** — source/config/tests support it but not independently executed.
- **Author claim** — stated by maintainer without adequate verification.
- **Inference** — reasoned conclusion from available evidence.
- **Insufficient evidence** — cannot support a conclusion.

Confidence describes certainty in the evaluation, not quality of the skill.
