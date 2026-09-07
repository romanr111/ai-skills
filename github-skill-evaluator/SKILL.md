---
name: github-skill-evaluator
description: Find, evaluate, compare, rank, and recommend open-source GitHub Agent Skills for Claude Code, OpenAI Codex, and other skill-capable agents. Use for discovering skills or assessing supplied repositories for intrinsic quality, fit, evidence that they deliver their promises, activation reliability, capability uplift, reusability, safety, maintainability, or complementary stacks. Search broadly when candidates are not supplied; inspect implementation and validate claims instead of relying on README polish or GitHub popularity.
---

# GitHub Skill Evaluator

Find and evaluate Agent Skills as executable knowledge systems, not popularity contests.

## Core principles

1. Search broadly, then inspect deeply. Search order is not quality.
2. Inspect the actual `SKILL.md` and material behavior-defining files before judging.
3. Separate author claims from evidence that the skill delivers those claims.
4. Bind every scored judgment to inspected evidence; abstain when evidence is insufficient.
5. Separate intrinsic quality from fit for the requested use case.
6. Capability uplift is model-relative. `strong` or `exceptional` uplift requires a recorded baseline probe.
7. Treat stars/forks/community signals as weak secondary context only.
8. Measure what can be measured: context volume, file existence, tests/probes, trigger cases.
9. Do not reward verbosity, repository size, number of scripts, or architectural complexity by themselves.
10. The normalized score is a secondary summary, not ranking truth.

## Evaluation depth

Use the cheapest depth that can answer the decision:

- **Triage** — broad discovery pool. Inspect entry point, direct references, license/reuse status, core workflow, compatibility, obvious evidence, and major red flags. **Do not score.**
- **Standard** — default for shortlisted candidates. Apply the 10-dimension evidence-bound rubric, promise-to-proof review, and mandatory counter-case.
- **Deep / benchmark** — use when the user asks for rigorous verification, a core claim is disputed, candidates are close, or risk is high. Add safe reproduction, representative probes, and adversarial cases where feasible.

Do not run untrusted code merely to increase confidence.

## Workflow

### 1. Parse the decision

Identify:
- supplied repositories/skills;
- intended use case, if any;
- discovery vs single evaluation vs comparison/ranking vs stack selection;
- constraints: agent/runtime, tools, OS, language, license, environment, offline requirements.

No use case is required for intrinsic evaluation. If absent, omit the fit score.

### 2. Discover candidates when needed

If the user asks to find/discover/recommend/best without a complete candidate set, read [references/discovery.md](references/discovery.md).

Use multiple query families across domain terms, job-to-be-done terms, ecosystem terms (`Agent Skill`, `Claude Code skill`, `Codex skill`, `SKILL.md`), and synonyms. Use repository and code/file search when available.

Build a broad pool, deduplicate forks/copies, check license/reuse eligibility, intentionally include credible lower-popularity candidates, and triage to a decision-relevant shortlist.

### 3. Define the evaluation unit and inspect

Read [references/repository-inspection.md](references/repository-inspection.md).

If evaluating one skill inside a multi-skill repository, score that skill plus its direct/shared dependencies. Repository-wide license/health may affect it; unrelated sibling skills must not inflate expertise/workflow/evidence.

Inspect, as relevant:
- `SKILL.md` and direct references;
- scripts/prompts/templates/agents/hooks/MCP/config;
- tests/evals/fixtures/examples/CI;
- dependencies/installation/license;
- commits/releases/issues/PRs where they answer a material question.

Stop when additional files are unlikely to change the decision.

When local files are available, run:

```bash
python3 scripts/repo_inventory.py /path/to/skill
```

Use its `context_cost` measurements for Context efficiency. The inventory is navigation/measurement, not a quality score.

### 4. Validate promises

Read [references/claim-validation.md](references/claim-validation.md).

Extract only material/core promises and create a compact ledger:

`promise → proof required → evidence found → status → limitation`

Use: `Verified`, `Supported`, `Plausible`, `Unproven`, `Contradicted`, or `Not testable here`.

Presence of tests/evals does not prove effectiveness unless they measure the promised outcome.

### 5. Apply the evidence-bound rubric

Read [references/evaluation-rubric.md](references/evaluation-rubric.md).

At Standard/Deep depth score exactly these 10 dimensions using bands:

- Activation & scope
- Instruction & workflow quality
- Domain expertise
- Verification & self-correction
- Capability uplift
- Evidence of effectiveness
- Safety & failure modes
- Reusability & composability
- Context efficiency
- Maintainability & docs

Bands are:
`absent | weak | adequate | strong | exceptional | insufficient_evidence`

For every scored band attach:
- repository-relative evidence path;
- quote, line range, or concrete observation;
- concise reasoning.

Use `insufficient_evidence` instead of inventing confidence. Abstained dimensions drop from the weighted total; report coverage.

When a local/materialized checkout exists, save the evaluation record as JSON and run:

```bash
python3 scripts/score_skill.py evaluation.json
```

The script validates evidence paths/quotes, band legality, coverage, counter-case structure, probe gating, confidence caps, tier caps, rubric version, and arithmetic. The script never decides whether a judgment is substantively good.

Always record the judge model because judgments are model-relative.

### 6. Apply the relevant domain/runtime overlay

Read [references/domain-overlays.md](references/domain-overlays.md) only for relevant sections.

For Claude Code-targeted skills, inspect activation/runtime specifics such as `.claude/skills`, invocation controls, tool permissions, subagent context, plugin packaging, portable paths, and CLAUDE.md interaction.

### 7. Probe capability uplift when warranted

Do not estimate `strong`/`exceptional` uplift by introspection.

- `adequate` or lower may be **Inferred** from concrete procedure/knowledge/tooling.
- `strong` requires at least one recorded same-task with-skill vs same-model baseline probe, judged blind when feasible.
- `exceptional` requires at least three runs/cases and should remain rare.

A one-run probe is directional evidence, not a benchmark.

### 8. Mandatory falsification pass

Every Standard/Deep evaluation must include a `counter_case`:

- strongest honest argument that the skill is worse/less useful than scored;
- dimensions at risk;
- a concrete observation that would change the verdict.

If you cannot articulate a serious counter-case, the evaluation is probably one-sided.

### 9. Fit for purpose

When a use case exists, separately score fit based on:
- problem match;
- agent/tool/stack compatibility;
- workflow match;
- unique capability contribution;
- integration/context cost;
- constraints/conflicts;
- expected uplift for this use case.

A strong skill can have low fit. Do not alter intrinsic quality because fit is low.

### 10. Compare and rank

Finish independent Standard evaluations before ranking.

Use:
- promise fulfillment;
- evidence-bound bands;
- coverage/confidence;
- fit;
- observed/inferred uplift;
- safety/reuse risk;
- decisive qualitative differences.

Do not let 1–3 score points decide a ranking by themselves. Treat close results as near-ties unless evidence identifies a decisive advantage.

For skill stacks use:

`Combined Value = Complementarity + Unique Capability - Redundancy - Instruction Conflict - Context Cost`

Do not simply choose the top two individual scores.

### 11. Adversarial calibration

Before finalizing, check:
- Did popularity/search order influence me?
- Did I score anything without inspected evidence?
- Did I mistake README claims or the existence of eval files for effectiveness?
- Did I give uplift above `adequate` without a baseline probe?
- Did I penalize justified specialization?
- Did I evaluate the named skill rather than sibling repository polish?
- Did I compare candidates at similar decision-relevant depth?
- Is the score coverage high enough to be meaningful?
- Is the counter-case substantive?
- Are score differences actually decision-relevant?

Correct the result if needed.

## Output

Read [references/output-format.md](references/output-format.md).

Lead with:
- promise fulfillment;
- recommendation;
- confidence;
- coverage;
- capability uplift (`Probed` or `Inferred`);
- only then the secondary intrinsic score/tier;
- rubric version and judge model.

For comparisons, start with the ranking table, then explain decisive evidence, uncertainty, redundancy/conflicts, and stack compatibility.
