# Domain Overlays

Use only relevant sections. Overlays refine the universal rubric; they do not add a second arbitrary total.

## Software architecture
Inspect coupling/cohesion, dependency direction, boundaries, evolvability, migration strategy, data/failure boundaries, testing implications, trade-offs, appropriate SOLID/pattern use, and overengineering resistance.

## Code review
Inspect defect prioritization, evidence tied to behavior/file/line, severity calibration, false-positive control, scope boundaries, test adequacy, deduplication, and actionable findings.

## Testing / QA
Inspect risk-based selection, deterministic assertions, isolation/data management, integration/E2E boundaries, flake diagnosis, coverage quality, failure triage, property/fuzz/contract testing where appropriate, and meaningful acceptance criteria.

## Security
Inspect threat/trust boundaries, exploitability evidence, severity, authn/authz, secret handling, dependency/supply-chain analysis, safe proof-of-concept boundaries, and remediation validation.

## DevOps / infrastructure
Inspect idempotency, rollback/recovery, environment separation, drift/config handling, observability, secrets, least privilege, failure domains, and deployment verification gates.

## Frontend / web design
Inspect hierarchy, typography, spacing, responsive behavior, accessibility, interaction states, motion purpose/reduced motion, component/design-system consistency, browser verification, and resistance to generic AI aesthetics.

## Visual QA
Inspect screenshot/reference comparison, multiple viewports, interaction/state coverage, structural vs pixel differences, regression methodology, accessibility, fix→recapture→compare loops, and objective completion criteria.

## Product design / UX
Inspect user/job framing, task flow, states/errors, information architecture, accessibility, interaction cost, recovery, research/evidence separation, design-system consistency, and usability validation.

## Research
Inspect source hierarchy, primary-source preference, citations, freshness, contradiction resolution, reproducible search, uncertainty, and fact/claim/inference separation.

## Writing / communication
Inspect audience/goal, source-fact preservation, tone/format control, structural editing, factuality, revision criteria, and resistance to generic AI voice.

## Data analysis
Inspect schema/data validation, missingness/outliers, reproducibility, statistical assumptions, leakage/confounding, uncertainty/sensitivity, traceable transformations, and visualization appropriateness.

## Business workflows
Inspect objective/decision linkage, measurable outputs, boundaries, exception/escalation handling, auditability, permissions/human approval, integrations, and value/ROI measurement where relevant.

## Agent-skill runtime / Claude Code

When evaluating a skill intended for Claude Code, inspect runtime behavior in addition to portable Agent Skills content:

- activation description quality and realistic over/under-trigger risk;
- project `.claude/skills/` versus personal `~/.claude/skills/` placement and whether intended sharing scope is clear;
- optional invocation controls such as `disable-model-invocation` when automatic activation would be unsafe or noisy;
- `context: fork` only when isolated subagent execution fits an actionable task;
- `allowed-tools` / permission scoping when the skill executes tools, especially destructive or external-impact operations;
- use of `${CLAUDE_SKILL_DIR}` or equivalent portable paths instead of fragile current-directory assumptions;
- plugin packaging (`skills/` in plugin root) when distribution is claimed;
- interaction with `CLAUDE.md`: CLAUDE.md is always-on project context while skill bodies load on demand; avoid duplicating large always-on instructions inside the skill;
- progressive disclosure because loaded skill content remains in context after invocation;
- trigger tests containing both should-trigger cases and adjacent near-miss should-not-trigger cases.

Do not require Claude-specific fields for a skill claiming only portable Agent Skills compatibility. Score them only when Claude Code support is part of the promise or use case.

## Unknown/new domains
Derive a lightweight overlay:
1. common expert failure modes?
2. evidence of correctness?
3. deterministic steps?
4. specialist decisions?
5. safety/legal constraints?
6. what would a frontier model likely miss?

Do not invent standards you cannot verify.
