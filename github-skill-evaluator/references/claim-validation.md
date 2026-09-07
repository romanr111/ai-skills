# Promise-to-Proof Validation

Use this protocol to answer the central question:

> Does the skill have credible evidence that it can deliver what it promises?

Do not treat implementation quality and promise validation as the same thing. A well-designed skill can have unproven outcome claims; a modest skill can accurately deliver a narrow promise.

## 1. Extract material promises

After inspecting implementation, collect only decision-relevant claims from the repository's README, skill description, examples, docs, benchmarks, releases, or maintainer statements.

Classify each claim as one of:
- **Capability** — “can perform X”, “supports Y workflow”.
- **Quality/reliability** — “production-ready”, “high-confidence”, “self-correcting”.
- **Outcome/benchmark** — “reduces defects”, “2× faster”, “improves conversion/design quality”.
- **Compatibility** — works with specific agents, stacks, operating systems, tools, or versions.
- **Portability/reuse** — reusable across projects/providers/environments.
- **Safety** — non-destructive, sandboxed, privacy-preserving, approval-gated.

Ignore purely promotional adjectives unless they imply a testable capability.

## 2. Build a promise-to-proof matrix

Maintain a compact matrix for the material claims:

| Promise | Importance | Proof required | Evidence found | Status | Limitation |
|---|---|---|---|---|---|
| Generates responsive UI | Core | workflow + realistic execution/example | skill + example | Supported | example not independently rerun |
| 2× faster than baseline | Core | controlled benchmark with defined baseline | README only | Unproven | no benchmark methodology |
| Works on Windows | Secondary | portable implementation or Windows test | POSIX shell script | Contradicted/unsupported | no Windows path |

Prioritize **core promises**: if false, the reason to install the skill disappears.

## 3. Status labels

Use these labels precisely:

- **Verified** — directly executed, reproduced, or independently confirmed in a way that tests the claim.
- **Supported** — repository implementation/tests strongly support the claim, but the evaluator did not independently reproduce it.
- **Plausible** — implementation is consistent with the claim, but evidence is incomplete.
- **Unproven** — claim is material but no adequate evidence was found.
- **Contradicted** — available evidence conflicts with the claim.
- **Not testable here** — claim requires an unavailable environment, account, proprietary dependency, hardware, or external condition.

Repeated author statements do not upgrade a claim from `Unproven` to `Supported`.

## 4. Validation ladder

Use the cheapest reliable level that can resolve the decision. Do not execute untrusted code merely to increase confidence.

### Level 0 — Static claim/implementation match

Check whether the promised behavior actually appears in:
- `SKILL.md` workflow;
- referenced procedures;
- scripts/configuration;
- expected outputs;
- constraints and tool integrations.

If a core promise has no implementation path, treat that as strong negative evidence.

### Level 1 — Test/eval inspection

Inspect tests/evals for:
- whether they exercise the promised capability rather than trivial parsing/formatting;
- realistic inputs and failure cases;
- meaningful assertions;
- baseline/comparator when improvement is claimed;
- cherry-picking or leakage;
- whether examples are generated fixtures presented as independent evidence.

Presence of an `evals/` directory is not itself effectiveness evidence.

### Level 2 — Deterministic reproduction

When safe and feasible, run repository-provided validation in an isolated/local environment.

Record:
- command/environment;
- result;
- failures/skips;
- whether the test actually maps to the claim.

Do not run scripts that request secrets, broad filesystem access, production credentials, remote mutation, or suspicious install hooks without explicit justification and safeguards.

### Level 3 — Representative smoke task

When the skill's output can be evaluated safely, run a small representative task that matches the claimed job-to-be-done.

Judge against observable acceptance criteria, not subjective “looks good” language.

Examples:
- code review → seeded defects and false-positive control;
- visual QA → known screenshot/layout differences across viewports;
- research → known source-quality/freshness traps;
- data analysis → known schema/statistical failure cases.

### Level 4 — Baseline or competitor A/B

Use when the repository claims meaningful uplift or when top candidates are close.

Compare:
- same task/input;
- same model/tool environment where possible;
- skill enabled versus baseline without the skill, or versus a competing skill;
- predefined success criteria;
- multiple cases when stochastic model behavior matters.

Do not claim causal uplift from one cherry-picked demonstration.

### Level 5 — Adversarial/failure-case validation

For high-risk or high-confidence claims, test likely failure modes:
- ambiguous input;
- missing dependency/tool;
- unsafe/destructive edge cases;
- contradictory instructions;
- domain-specific traps;
- out-of-distribution cases.

## 5. Benchmark validity checks

For any numerical performance/outcome claim, ask:
- Is the metric defined?
- Is the baseline defined and fair?
- Does the benchmark task match the claimed real-world use?
- Are model/version/tool settings comparable?
- Is sample size/repetition adequate for stochastic outputs?
- Are failed cases and variance reported?
- Could the benchmark be contaminated, cherry-picked, or tuned to the skill?
- Can the result be reproduced from available materials?

If these are missing, label the numerical claim `Unproven` even if the skill itself is otherwise strong.

## 6. Overall promise fulfillment

Summarize core promises using one of:
- **Verified** — core promises independently validated or strongly reproduced.
- **Supported** — core promises map well to implementation and meaningful repository evidence.
- **Partially supported** — some core promises have evidence, others remain unproven.
- **Unproven** — central value proposition lacks adequate evidence.
- **Contradicted** — one or more central promises conflict with observed behavior/evidence.

This is not a replacement for the 0–100 quality score. Report both when promise fulfillment is material.

## 7. Relationship to scoring

Feed the result primarily into:
- **Evidence of effectiveness**;
- **Verification and self-correction**;
- **Reusability** for portability/compatibility claims;
- **Safety** for safety claims;
- **Model leverage / capability uplift** for claimed incremental value.

Do not double-penalize the same missing evidence across every dimension. Penalize where causally relevant and explain the main effect once.

A strong unsupported marketing claim should lower evidence confidence, not automatically erase genuine intrinsic quality. A contradicted **core** promise is more serious and may materially lower the overall recommendation.
