# Promise-to-Proof Validation

Use this protocol to answer:

> Does the skill have credible evidence that it can deliver what it promises?

Do not conflate implementation quality with promise validation. A strong implementation can still make unproven outcome claims.

## Extract material promises

After implementation inspection, collect only decision-relevant claims from README, skill description, docs, examples, benchmarks, releases, or maintainer statements.

Classify:
- **Capability** — can perform X / supports Y workflow
- **Quality/reliability** — production-ready, high-confidence, self-correcting
- **Outcome/benchmark** — faster, more accurate, fewer defects, better quality
- **Compatibility** — agents, stacks, OSes, tools, versions
- **Portability/reuse** — cross-project/provider/environment reuse
- **Safety** — non-destructive, sandboxed, approval-gated

## Promise-to-proof matrix

| Promise | Importance | Proof required | Evidence found | Status | Limitation |
|---|---|---|---|---|---|

Prioritize **core promises**: if false, the reason to install the skill disappears.

Statuses:
- **Verified** — independently executed/reproduced/confirmed against the claim
- **Supported** — implementation/tests strongly support it, not independently reproduced
- **Plausible** — consistent implementation, incomplete evidence
- **Unproven** — material claim lacks adequate evidence
- **Contradicted** — available evidence conflicts with the claim
- **Not testable here** — required environment/dependency is unavailable

Repeated author claims do not upgrade evidence.

## Validation ladder

Use the cheapest safe level that can change the decision.

### Level 0 — Static implementation match
Check whether the promised behavior exists in the actual workflow, references, scripts, config, outputs, and constraints.

### Level 1 — Test/eval inspection
Check whether tests measure the promised behavior rather than presence of headings, files, or implementation details.

### Level 2 — Deterministic reproduction
When safe and feasible, run repository-provided validation in an isolated/local environment. Record command, environment, result, failures/skips, and claim mapping.

### Level 3 — Representative smoke task
Run a small task that matches the job-to-be-done with observable acceptance criteria.

### Level 4 — Capability-uplift probe
Use this when evaluating incremental value over a frontier-model baseline.

Run the **same representative task** with:
1. the skill enabled;
2. the same model/tool environment without the skill.

Persist both outputs before judging. The scorer validates that the referenced artifacts exist and are distinct; this prevents a `strong` uplift claim from being backed only by descriptive strings.

Record:

```json
{
  "uplift_probe": {
    "task": "representative task",
    "probe_root": "/absolute/path/to/probe-artifacts",
    "with_skill_output": "with-skill/output.txt",
    "baseline_output": "baseline/output.txt",
    "execution_model": "model-id-used-for-both-arms",
    "same_model_environment": true,
    "judged_blind": true,
    "judge_verdict": "with-skill materially better on X; equal on Y",
    "runs": 1
  }
}
```

Rules:
- `probe_root` must exist; output paths are relative to it and must resolve to existing, different files or directories.
- `same_model_environment: true` means task, model, tool access, and material execution settings were held constant except for the skill being enabled.
- `strong` capability uplift requires at least one valid recorded probe.
- `exceptional` requires at least three runs/cases and should remain rare.
- one probe is directional evidence, not a benchmark.
- without a valid probe, uplift cannot exceed `adequate` and must be labeled **Inferred**.
- the scorer can enforce artifact existence and declared comparability, but it cannot prove the evaluator actually blinded itself or that the declaration is truthful; preserve that limitation in confidence language.

### Level 5 — Adversarial/failure-case validation
For high-risk or high-confidence claims, test ambiguous input, missing dependencies, unsafe edges, contradictions, and domain-specific traps.

## Numerical benchmark validity

For every quantitative outcome claim ask:
- metric defined?
- fair baseline defined?
- representative task/data?
- model/version/tool settings comparable?
- enough repetitions for stochastic output?
- variance/failures reported?
- cherry-picking or tuning risk?
- reproducible materials?

If not, label the numerical claim `Unproven` even if intrinsic quality is strong.

## Overall promise fulfillment

Use:
- **Verified**
- **Supported**
- **Partially supported**
- **Unproven**
- **Contradicted**

Report this separately from the rubric score.

## Scoring relationship

Feed promise evidence primarily into:
- Evidence of effectiveness
- Verification & self-correction
- Reusability & composability for compatibility/reuse claims
- Safety & failure modes for safety claims
- Capability uplift for incremental-value claims

Do not double-penalize one missing piece of evidence across every dimension.
