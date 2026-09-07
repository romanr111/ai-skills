---
name: github-skill-evaluator
description: Evaluate, compare, rank, and recommend open-source GitHub Agent Skills for reuse by Claude Code, OpenAI Codex, and other skill-capable agents. Use when assessing one or more skill repositories for intrinsic quality, fit for a specific workflow, capability uplift over a frontier-model baseline, reusability, engineering rigor, evidence, maintainability, safety, or when choosing a complementary skill stack. Inspect repository contents rather than relying on README polish or GitHub popularity.
---

# GitHub Skill Evaluator

Evaluate Agent Skills as executable knowledge systems, not popularity contests.

## Core principles

1. Inspect evidence before scoring. Read the actual `SKILL.md` and material references, scripts, tests/evals, examples, configuration, and repository signals.
2. Separate **intrinsic quality** from **fit for the requested use case**.
3. Estimate **capability uplift**: how much a strong current frontier agent improves with the skill versus without it.
4. Treat stars, forks, watchers, contributor count, and social mentions as weak secondary evidence only.
5. Distinguish `Verified`, `Supported by repository evidence`, `Author claim`, `Inference`, and `Insufficient evidence`.
6. Do not reward verbosity, repository size, number of scripts, or architectural complexity by themselves.
7. Compare candidates independently before ranking to reduce anchoring.
8. If evidence is missing, lower confidence; do not automatically lower quality unless the absence itself is a meaningful quality defect.

## Required workflow

### 1. Parse the decision

Identify:
- repositories or individual skills to evaluate;
- intended use case, if supplied;
- whether the task is single-skill evaluation, comparison, ranking, or stack selection;
- material constraints such as model, tools, operating system, language, or environment.

Do not require a use case for intrinsic evaluation. If none is supplied, omit the fit score or label fit as `Not specified`.

### 2. Inspect the repository

First define the **evaluation unit**. If the user names one skill inside a multi-skill repository, score that skill's behavior and supporting files; use repository-wide health/license metadata only as supporting context. Do not let strong sibling skills inflate the target skill.

Read [references/repository-inspection.md](references/repository-inspection.md) for the inspection protocol. Inspect comparable depth for every candidate. At minimum seek:
- `SKILL.md` and other skills;
- directly referenced Markdown or reference files;
- scripts, prompts, templates, agents, hooks, MCP/config files;
- tests, evals, fixtures, examples, CI;
- dependencies and installation requirements;
- license;
- recent commits, releases, material issues/PRs when useful.

Follow a reference only when it materially affects behavior or evidence. Do not recursively load irrelevant documentation.

If local repository access is available, optionally run:

```bash
python3 scripts/repo_inventory.py /path/to/repo
```

Use the inventory as navigation aid, not as a quality score.

### 3. Establish evidence strength

Build a small internal evidence ledger before scoring: `claim/dimension → source path or observation → evidence label → limitations`. This prevents README claims from silently becoming facts.

Classify evidence before scoring:
- **Strong**: evals, benchmarks, repeatable tests, before/after comparisons, measured outcomes, independent validation.
- **Moderate**: realistic worked examples, real usage, issue/PR evidence, active maintenance, reproducible demonstrations.
- **Weak**: README claims, screenshots without methodology, stars, marketing language.
- **None**: no meaningful effectiveness evidence found.

Separate evidence of effectiveness from repository popularity.

### 4. Score the universal rubric

Read [references/evaluation-rubric.md](references/evaluation-rubric.md). Score all 18 dimensions from 0–10 using the defined weights. Use integer or half-point dimension scores; report the normalized overall score as an integer unless precision is genuinely useful.

If scripts are absent or irrelevant, score **Code/script quality** based on whether omitting scripts is appropriate rather than penalizing absence mechanically.

For deterministic arithmetic, save scores to JSON and run:

```bash
python3 scripts/score_skill.py scores.json
```

### 5. Apply a domain overlay

Read [references/domain-overlays.md](references/domain-overlays.md) only for the relevant domain. Use the overlay to interpret universal dimensions and expose domain-specific failure modes; do not create a second arbitrary total unless the user explicitly requests one.

### 6. Estimate frontier-model baseline and uplift

Ask:

> What concrete capability, procedure, constraint, tool, or specialist knowledge does this skill add beyond what a strong current frontier model would reliably do from the user's task alone?

Classify uplift:
- **Transformative**: enables a workflow or reliability level that is otherwise difficult to achieve.
- **High**: materially improves consistency, correctness, or efficiency across repeated use.
- **Moderate**: useful, repeatable improvement with meaningful but bounded benefit.
- **Low**: mostly convenience, reminders, or modest structure.
- **Negligible**: generic advice or behavior already reliably present in the baseline model.

Do not infer uplift from skill length.

### 7. Detect red flags and caps

Read [references/red-flags.md](references/red-flags.md). Report material red flags explicitly.

Apply quality caps when warranted:
- critical unsafe/destructive behavior without safeguards: maximum `D` unless the dangerous behavior is the explicit intended domain and is properly controlled;
- malicious, deceptive, plagiarized-with-unclear-provenance, or functionally broken: `F`;
- cannot execute because required private/unavailable dependencies are undocumented: maximum `C` for general reusability;
- no license for a repository intended for reuse: flag legal reuse uncertainty; do not automatically assign `F`.

### 8. Fit-for-purpose

When a use case is supplied, separately score `Fit for This Use Case: 0–100` based on:
- problem match;
- stack/tool compatibility;
- workflow match;
- unique capability contribution;
- integration cost;
- constraints/conflicts;
- expected uplift for this use case.

A high-quality skill may have low fit. Do not let fit alter intrinsic quality.

### 9. Compare and rank

For multiple candidates:
1. finish each independent evaluation first;
2. compare score, evidence, uplift, risks, and fit;
3. explain why the winner beats the runner-up;
4. avoid unsupported microscopic score differences;
5. identify whether score differences are within uncertainty.

Use practical uncertainty, not fake statistical confidence. As a default, treat gaps under ~3 points as a near-tie unless there is a decisive qualitative difference; with Low confidence, even larger gaps may be non-decisive. Prefer explaining the decisive evidence over manufacturing score precision.

For stacks, do not simply choose the top two. Use:

`Combined Value = Complementarity + Unique Capability - Redundancy - Instruction Conflict - Context Cost`

Report each skill's responsibility, overlap, conflicts, and activation order when relevant.

### 10. Adversarial calibration

Before finalizing, verify:
- Am I rewarding popularity, README polish, or repository size?
- Am I mistaking complexity for sophistication?
- Am I penalizing justified specialization?
- Am I rewarding generic advice a frontier model already knows?
- Did I inspect the actual `SKILL.md` and material references?
- Did I distinguish author claims from verified evidence?
- Did I compare candidates at comparable depth?
- Am I accidentally scoring repository-wide polish instead of the named skill?
- Are score differences supported by evidence?
- Could a less popular candidate be better?
- Did I keep intrinsic quality separate from fit?

Correct the scores/ranking if this review exposes bias.

## Output

Use [references/output-format.md](references/output-format.md). Be concise by default, but show enough evidence to make the decision auditable.

For a single skill always include:
- intrinsic score and tier;
- fit score when use case exists;
- capability uplift;
- confidence;
- evidence strength;
- strongest advantages;
- weaknesses/red flags;
- recommendation.

For comparisons, start with the ranking table, then explain the decisive differences and stack compatibility.

## Confidence

Use:
- **High**: deep repository inspection plus tests/evals or strong reproducible evidence; no major inaccessible components.
- **Medium**: source inspected well but effectiveness evidence is incomplete, or some material components could not be validated.
- **Low**: limited repository access, missing source, inaccessible dependencies, or conclusions rely heavily on claims/inference.

Never convert lack of evidence into a claim of poor quality without explaining the distinction.
