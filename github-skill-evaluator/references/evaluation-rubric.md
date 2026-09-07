# Evaluation Rubric

**Rubric version:** `2026-09-v2`

This rubric deliberately uses **five anchored bands**, not 0–10 scores. The model judges; the scorer only validates evidence, abstention, probe requirements, coverage, caps, and arithmetic.

## Scoring rules

Each dimension must be one of:

- `absent` = 0.00
- `weak` = 0.25
- `adequate` = 0.50
- `strong` = 0.75
- `exceptional` = 1.00
- `insufficient_evidence` = abstain; the dimension drops out and remaining weights renormalize

For every scored band, attach evidence from material actually inspected: a repository-relative `path` plus a quote, line range, or concrete observation. Do not score from README reputation, stars, or memory.

Abstention is legitimate. Use `insufficient_evidence` when the repository or available environment does not support a judgment. Coverage must be reported.

`score = Σ(band_value × weight) / answered_weight × 100`

Coverage confidence caps:
- coverage < 85% → confidence cannot exceed `Medium`
- coverage < 70% → confidence cannot exceed `Low`

The numeric score is a **secondary summary**, not ranking truth. Do not use tiny score gaps as decisive evidence.

## Weights

| # | Dimension | Weight |
|---:|---|---:|
| 1 | Activation & scope | 10% |
| 2 | Instruction & workflow quality | 13% |
| 3 | Domain expertise | 12% |
| 4 | Verification & self-correction | 12% |
| 5 | Capability uplift *(probe-gated)* | 15% |
| 6 | Evidence of effectiveness | 10% |
| 7 | Safety & failure modes | 10% |
| 8 | Reusability & composability | 8% |
| 9 | Context efficiency *(measure first)* | 5% |
| 10 | Maintainability & docs | 5% |
|  | **Total** | **100%** |

Popularity is only a minor supporting input inside Maintainability & docs. It is never proof of quality.

## Band anchors

### 1. Activation & scope — 10%
Assess trigger description, intended task, non-goals, false-positive/false-negative activation risk, scope boundaries, and whether the skill knows when not to activate.
- `absent` — no reliable activation boundary or the skill routinely targets the wrong task.
- `weak` — broad keywords and intent exist, but adjacent near-misses are likely to trigger incorrectly.
- `adequate` — common intended prompts should activate correctly; meaningful edge/near-miss gaps remain.
- `strong` — clear positive and negative boundaries, realistic trigger wording, and low obvious over/under-trigger risk.
- `exceptional` — activation has realistic should-trigger and near-miss testing, held-out validation, or equivalent evidence showing reliable routing.

### 2. Instruction & workflow quality — 13%
Assess clarity, sequencing, branching, stop criteria, decision rules, inspection-before-action, escalation, proportionality, and useful systems thinking.
- `absent` — instructions are contradictory, non-executable, or actively harmful.
- `weak` — mostly goals, slogans, or generic advice without an operational path.
- `adequate` — usable sequence exists, but branches, edge cases, or completion criteria are incomplete.
- `strong` — workflow materially constrains execution with clear branches, priorities, stop conditions, and trade-offs.
- `exceptional` — unusually crisp operational design converts complex expertise into a robust, low-ambiguity procedure with strong proportionality.

### 3. Domain expertise — 12%
Assess non-obvious heuristics, standards, specialist failure modes, trade-offs, terminology, and knowledge a frontier model would not reliably reconstruct every run.
- `absent` — material domain claims are wrong or no domain substance exists.
- `weak` — generic best practices presented as expertise.
- `adequate` — correct useful domain knowledge with some non-obvious criteria, but limited depth or failure-mode coverage.
- `strong` — specialist heuristics, trade-offs, constraints, and failure modes materially improve decisions.
- `exceptional` — rare, domain-leading operational knowledge with nuanced exceptions and high-value expert judgment that would be difficult to reconstruct ad hoc.

### 4. Verification & self-correction — 12%
Assess acceptance criteria, tests, assertions, independent checks, adversarial review, fix/recheck loops, and whether bundled scripts/tests validate claimed behavior.
- `absent` — output is generated and trusted, or validation is misleading.
- `weak` — says “check/test/review” without observable criteria or meaningful assertions.
- `adequate` — some concrete validation exists, but important failure modes or independent checks are missing.
- `strong` — verification is first-class, tied to likely failure modes, and includes explicit done criteria or repeatable checks.
- `exceptional` — multiple independent validation layers, realistic failure cases, and self-correction loops demonstrably catch errors rather than formatting defects.

### 5. Capability uplift — 15%
Assess incremental value over a strong current frontier model. This dimension is **probe-gated**.
- `absent` — adds no meaningful capability or degrades baseline behavior.
- `weak` — mostly reminders, formatting, or behavior the baseline model already performs reliably.
- `adequate` — plausible repeatable improvement from concrete procedure/knowledge/tooling; may be inferred without a probe.
- `strong` — requires at least one recorded same-task with-skill vs baseline probe judged blind; observed improvement is material on decision-relevant criteria.
- `exceptional` — rare; repeated probe evidence across at least three runs/cases shows large, robust uplift with no material offsetting regression.
Without a valid probe, `strong` and `exceptional` are invalid.

### 6. Evidence of effectiveness — 10%
Assess whether the repository demonstrates that the skill delivers its core promises.
- `absent` — no relevant evidence or available evidence contradicts the core value proposition.
- `weak` — author claims, screenshots, examples, or tests that do not measure the promised outcome.
- `adequate` — realistic examples or meaningful repository tests support part of the promise, but comparative/field evidence is limited.
- `strong` — repeatable evals, defect-seeded cases, meaningful before/after evidence, measured outcomes, or independent real-world validation support core promises.
- `exceptional` — unusually rigorous, reproducible, representative evidence with fair baselines, repeated cases, failure reporting, and independent corroboration.

### 7. Safety & failure modes — 10%
Assess destructive behavior, permissions, secrets, remote execution, supply-chain exposure, confirmations, rollback/recovery, silent failure, and overconfident automation.
- `absent` — severe uncontrolled unsafe behavior or deceptive/malicious operation.
- `weak` — material risks exist with vague or missing safeguards.
- `adequate` — common risks are addressed, but important edge cases, confirmations, or recovery paths remain incomplete.
- `strong` — clear risk boundaries, least-privilege behavior, confirmations/rollback where needed, and domain-specific failure handling.
- `exceptional` — unusually strong safety design with explicit trust boundaries, reversible defaults, adversarial failure handling, and validated safeguards.
Severe conditions may cap the final tier regardless of arithmetic.

### 8. Reusability & composability — 8%
Assess portability, declared dependencies, project/provider/OS coupling, predictable inputs/outputs, responsibility boundaries, overlap, and conflicts with other skills.
- `absent` — cannot be reused outside its origin or hidden dependencies make execution impractical.
- `weak` — substantial undocumented coupling or destructive overlap with adjacent skills.
- `adequate` — reusable in the intended domain with some declared constraints and manageable integration cost.
- `strong` — portable, dependencies explicit, interfaces/boundaries clear, and it composes predictably with related workflows.
- `exceptional` — unusually clean portability across environments/providers with deliberate interoperability, low context conflict, and excellent adaptation guidance.
Do not penalize justified specialization.

### 9. Context efficiency — 5%
Measure first with `scripts/repo_inventory.py` when local files are available. Consider always-loaded `SKILL.md` bytes/lines/estimated tokens, on-demand reference volume, duplication, and behavioral utility per token.
- `absent` — context design is unusable: monolithic, highly duplicative, or excessive enough to undermine the task.
- `weak` — significant prompt bloat or poor progressive disclosure with little marginal behavioral value.
- `adequate` — reasonable size and structure; some duplication or avoidable always-loaded material remains.
- `strong` — concise entry point, progressive disclosure, high information density, and measured always-loaded cost is proportionate to value.
- `exceptional` — exceptionally efficient information architecture with tiny necessary always-loaded context and well-partitioned deterministic/reference resources.
A byte/token estimate is not itself quality; judge cost relative to behavioral value.

### 10. Maintainability & docs — 5%
Assess structure, naming, installation, expected inputs/outputs, dependencies, versioning, license, maintenance risk, troubleshooting, and only weakly community/adoption signals.
- `absent` — broken/unmaintainable packaging, missing critical setup information, or legal/reuse status blocks intended use.
- `weak` — difficult to install/understand, fragile structure, or important compatibility/version assumptions are undocumented.
- `adequate` — understandable and usable with normal maintenance/documentation gaps.
- `strong` — clear packaging, installation, version/reuse information, proportional modularity, and low maintenance risk.
- `exceptional` — exemplary maintainability with stable interfaces, disciplined versioning/changelog, excellent troubleshooting, and strong provenance/reuse clarity.

## Tiers
Use the secondary normalized score only after evidence validation and caps:
| Tier | Score | Meaning |
|---|---:|---|
| S | 90–100 | Exceptional; rare and strongly evidenced |
| A | 80–89 | Strong production-quality skill |
| B | 70–79 | Useful with meaningful limitations |
| C | 55–69 | Limited; significant weaknesses |
| D | 40–54 | Weak or high-risk |
| F | <40 | Avoid |

Coverage and promise fulfillment must appear beside any score. A low-coverage high score is provisional, not strong evidence.
