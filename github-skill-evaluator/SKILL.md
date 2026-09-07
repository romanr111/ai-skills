---
name: github-skill-evaluator
description: Find, evaluate, compare, rank, and recommend open-source GitHub Agent Skills for reuse by Claude Code, OpenAI Codex, and other skill-capable agents. Use when discovering skills for a workflow or assessing supplied repositories for intrinsic quality, fit, capability uplift, evidence that they deliver their promises, reusability, engineering rigor, maintainability, safety, or complementary stacks. Search broadly when candidates are not supplied; inspect repository contents and validate claims rather than relying on README polish or GitHub popularity.
---

# GitHub Skill Evaluator

Find and evaluate Agent Skills as executable knowledge systems, not popularity contests.

## Core principles

1. **Search broadly, then inspect deeply.** Search ranking is candidate discovery, not evaluation.
2. **Inspect evidence before scoring.** Read the actual `SKILL.md` and material references, scripts, tests/evals, examples, configuration, and repository signals.
3. **Verify promises explicitly.** Separate what the author claims from what implementation/tests or direct reproduction support.
4. Separate **intrinsic quality** from **fit for the requested use case**.
5. Estimate **capability uplift**: how much a strong current frontier agent improves with the skill versus without it.
6. Treat stars, forks, watchers, contributor count, and social mentions as weak secondary evidence only.
7. Distinguish `Verified`, `Supported`, `Plausible`, `Author claim`, `Inference`, `Unproven`, and `Contradicted` where useful.
8. Do not reward verbosity, repository size, number of scripts, or architectural complexity by themselves.
9. Compare candidates independently before ranking to reduce anchoring.
10. If evidence is missing, lower confidence; do not automatically equate missing evidence with poor intrinsic quality.

## Evaluation depth

Use the cheapest depth that can answer the decision:

- **Triage** — for broad discovery pools. Inspect entry point, direct references, license/reuse status, core workflow, obvious evidence, compatibility, and major red flags. Do not fully score every candidate.
- **Standard** — default for shortlisted candidates. Apply the complete rubric and promise-to-proof review.
- **Deep / benchmark** — use when the user asks for rigorous verification, a core claim is disputed, candidates are close, or risk is high. Reproduce safe tests and perform representative or A/B validation when feasible.

Do not run untrusted code merely to increase confidence.

## Required workflow

### 1. Parse the decision

Identify:
- repositories or individual skills already supplied;
- intended use case, if supplied;
- whether the task is discovery, single-skill evaluation, comparison, ranking, or stack selection;
- material constraints such as model, tools, operating system, language, license, environment, or offline requirements.

Do not require a use case for intrinsic evaluation. If none is supplied, omit the fit score or label fit as `Not specified`.

### 2. Discover candidates when needed

If the user asks to **find**, **discover**, **recommend**, or identify the **best** skills without providing a complete candidate set, read [references/discovery.md](references/discovery.md).

Use multiple query families spanning domain terms, job-to-be-done terms, agent ecosystem terms, and synonyms. Use repository and code/file search when available. Build a broad pool, deduplicate forks/copies, check open-source/reuse eligibility, then triage to a decision-relevant shortlist.

Do not simply take the most-starred or first search results. Include credible lower-popularity candidates when available.

### 3. Inspect the repository

First define the **evaluation unit**. If the user names one skill inside a multi-skill repository, score that skill's behavior and supporting files; use repository-wide health/license metadata only as supporting context. Do not let strong sibling skills inflate the target skill.

Read [references/repository-inspection.md](references/repository-inspection.md). Inspect comparable depth for every shortlisted candidate. At minimum seek:
- `SKILL.md` and direct behavior-defining references;
- scripts, prompts, templates, agents, hooks, MCP/config files;
- tests, evals, fixtures, examples, CI;
- dependencies and installation requirements;
- license/reuse status;
- recent commits, releases, material issues/PRs when useful.

Follow a reference only when it materially affects behavior or evidence. Do not recursively load irrelevant documentation.

If local repository access is available, optionally run:

```bash
python3 scripts/repo_inventory.py /path/to/repo
```

Use the inventory as navigation aid, not as a quality score.

### 4. Validate what the skill promises

Read [references/claim-validation.md](references/claim-validation.md).

After implementation inspection, extract the **material/core promises** from README/description/docs/examples and map each to evidence. Distinguish:
- capability claims;
- quality/reliability claims;
- numerical outcome/benchmark claims;
- compatibility/portability claims;
- safety claims.

Build a compact promise-to-proof ledger: `promise → proof required → evidence found → status → limitation`.

For central promises, use the strongest safe validation level justified by the decision:
1. static implementation match;
2. tests/evals inspection;
3. deterministic reproduction when safe;
4. representative smoke task;
5. baseline/competitor A/B when uplift is claimed or candidates are close;
6. adversarial failure-case validation for high-risk/high-confidence claims.

Never call a benchmark claim verified when its metric, baseline, methodology, or reproducibility is missing.

### 5. Establish evidence strength

Maintain a compact internal evidence ledger before scoring: `claim/dimension → source path or observation → evidence label → limitations`.

Classify overall evidence:
- **Strong**: repeatable evals/benchmarks, measured outcomes, reproduced tests/tasks, independent validation.
- **Moderate**: meaningful repository tests/evals, realistic worked examples, issue/PR evidence, reproducible demonstrations not independently rerun.
- **Weak**: mainly README claims, screenshots without methodology, usage anecdotes, popularity signals.
- **None**: no meaningful effectiveness evidence found.

Separate evidence of effectiveness from repository popularity.

### 6. Score the universal rubric

Read [references/evaluation-rubric.md](references/evaluation-rubric.md). Score all 18 dimensions from 0–10 using the defined weights for shortlisted candidates under Standard/Deep evaluation.

Use integer or half-point dimension scores; report the normalized overall score as an integer unless precision is genuinely useful.

If scripts are absent or irrelevant, score **Code/script quality** based on whether omitting scripts is appropriate rather than penalizing absence mechanically.

For deterministic arithmetic, save scores to JSON and run:

```bash
python3 scripts/score_skill.py scores.json
```

### 7. Apply the relevant domain overlay

Read [references/domain-overlays.md](references/domain-overlays.md) only for the relevant domain. Use the overlay to interpret universal dimensions and expose domain-specific failure modes; do not create a second arbitrary total unless the user explicitly requests one.

### 8. Estimate frontier-model baseline and uplift

Ask:

> What concrete capability, procedure, constraint, tool, or specialist knowledge does this skill add beyond what a strong current frontier model would reliably do from the user's task alone?

Classify uplift:
- **Transformative** — enables a workflow or reliability level otherwise difficult to achieve.
- **High** — materially improves consistency, correctness, or efficiency across repeated use.
- **Moderate** — useful repeatable improvement with bounded benefit.
- **Low** — mostly convenience, reminders, or modest structure.
- **Negligible** — generic behavior already reliable in the baseline model.

Do not infer uplift from skill length or author claims alone.

### 9. Detect red flags and caps

Read [references/red-flags.md](references/red-flags.md). Report material red flags explicitly.

Apply quality caps when warranted:
- critical unsafe/destructive behavior without safeguards: maximum `D` unless the dangerous behavior is the explicit domain and properly controlled;
- malicious, deceptive, plagiarized-with-unclear-provenance, or functionally broken: `F`;
- required private/unavailable dependencies are undocumented: maximum `C` for general reusability;
- no clear reuse license: flag legal reuse uncertainty; when the user explicitly requires open source, do not present it as fully reusable open source.

### 10. Fit-for-purpose

When a use case is supplied, separately score `Fit for This Use Case: 0–100` based on:
- problem match;
- stack/tool compatibility;
- workflow match;
- unique capability contribution;
- integration cost;
- constraints/conflicts;
- expected uplift for this use case.

A high-quality skill may have low fit. Do not let fit alter intrinsic quality.

### 11. Compare and rank

For multiple candidates:
1. triage the broad pool before expensive full scoring;
2. finish each shortlisted candidate's independent evaluation before ranking;
3. compare score, promise fulfillment, evidence, uplift, risks, and fit;
4. explain why the winner beats the runner-up;
5. avoid unsupported microscopic score differences;
6. identify when the result is within uncertainty.

As a default, treat gaps under ~3 points as a near-tie unless there is a decisive qualitative difference. With Low confidence, even larger gaps may be non-decisive.

For stacks, do not simply choose the top two. Use:

`Combined Value = Complementarity + Unique Capability - Redundancy - Instruction Conflict - Context Cost`

Report each skill's responsibility, overlap, conflicts, and activation order when relevant.

### 12. Adversarial calibration

Before finalizing, verify:
- Did I search more than one query family when discovery was required?
- Did search ranking, stars, README polish, or repository size bias the shortlist?
- Did I deduplicate forks/copies and check license/reuse status?
- Did I inspect the actual `SKILL.md` and material references?
- Did I extract the core promises and map them to evidence?
- Am I calling an author claim “verified” without reproduction or adequate tests?
- Do tests/evals actually measure the promised outcome?
- Am I mistaking complexity for sophistication?
- Am I penalizing justified specialization?
- Am I rewarding generic advice a frontier model already knows?
- Did I compare shortlisted candidates at comparable depth?
- Am I accidentally scoring repository-wide polish instead of the named skill?
- Are score differences supported by evidence?
- Could a less popular candidate be better?
- Did I keep intrinsic quality, fit, and promise fulfillment distinct?

Correct the shortlist, scores, or ranking if this review exposes bias.

## Output

Use [references/output-format.md](references/output-format.md). Be concise by default, but show enough evidence to make the decision auditable.

For a single skill include:
- intrinsic score and tier;
- fit score when a use case exists;
- **promise fulfillment** for core claims;
- capability uplift;
- confidence and evidence strength;
- strongest advantages;
- weaknesses/red flags;
- recommendation.

For discovery/rankings, start with the shortlist/ranking table, then explain decisive differences, promise evidence, and stack compatibility.

## Confidence

Use:
- **High**: deep repository inspection plus reproduced tests/evals or strong independently checkable evidence; no major inaccessible components.
- **Medium**: source inspected well and repository evidence is meaningful, but effectiveness or core promises were not fully reproduced.
- **Low**: limited repository access, missing source, inaccessible dependencies, or conclusions rely heavily on claims/inference.

Confidence describes certainty in the evaluation, not intrinsic quality. Never convert lack of evidence into a claim of poor quality without explaining the distinction.
