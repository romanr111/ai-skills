# Domain Overlays

Use only the relevant section(s). These overlays refine interpretation of the universal rubric; they do not replace it.

## Table of contents

1. Software architecture
2. Code review
3. Testing and QA
4. Security
5. DevOps / infrastructure
6. Frontend and web design
7. Visual QA
8. Product design / UX
9. Research
10. Writing / communication
11. Data analysis
12. Business workflows
13. Agent-skill runtime / Claude Code
14. Unknown/new domains

## 1. Software architecture

Inspect whether the skill operationalizes:
- coupling/cohesion and dependency direction;
- boundaries and ownership;
- evolvability and migration strategy;
- trade-offs rather than pattern dogma;
- appropriate use of SOLID/design patterns;
- data and failure boundaries;
- testing implications;
- avoidance of premature abstraction and cargo-cult architecture.

Red flags: architecture astronautics, blanket pattern mandates, rewrites without migration plan, no constraints or trade-offs.

## 2. Code review

Inspect:
- defect prioritization and severity calibration;
- evidence tied to file/line or concrete behavior;
- correctness/security/performance/maintainability balance;
- false-positive control;
- review scope boundaries;
- handling of tests and behavior changes;
- deduplication and actionable findings.

Red flags: style nitpicking presented as defects, unsupported claims, no severity model, no reproduction reasoning.

## 3. Testing and QA

Inspect:
- risk-based test selection;
- deterministic assertions;
- test isolation and data management;
- integration/E2E boundaries;
- flaky-test diagnosis;
- coverage quality rather than raw count;
- failure triage;
- appropriate property/fuzz/contract testing;
- meaningful acceptance criteria.

Red flags: maximizing test count, brittle selectors, snapshot-only validation, hidden nondeterminism.

## 4. Security

Inspect:
- threat modeling and trust boundaries;
- exploitability/evidence requirements;
- severity calibration;
- secret handling;
- dependency/supply-chain analysis;
- authn/authz distinctions;
- safe proof-of-concept boundaries;
- remediation validation.

Red flags: destructive exploitation by default, speculative vulnerabilities presented as confirmed, insecure secret handling.

## 5. DevOps / infrastructure

Inspect:
- idempotency;
- rollback and recovery;
- environment separation;
- drift/configuration handling;
- observability;
- secret management;
- least privilege;
- failure-domain awareness;
- safe deployment and verification gates.

Red flags: direct production mutation without safeguards, no rollback, environment assumptions, destructive defaults.

## 6. Frontend and web design

Inspect:
- hierarchy and information architecture;
- typography and spacing systems;
- responsive behavior;
- accessibility;
- interaction states;
- motion purpose and reduced-motion handling;
- component/design-system consistency;
- browser/runtime verification;
- avoidance of generic AI aesthetics when visual originality matters.

Red flags: purely aesthetic prose with no implementation/verification method, no responsive/accessibility criteria.

## 7. Visual QA

Inspect:
- screenshot/reference comparison;
- multiple viewport coverage;
- interaction and state coverage;
- structural versus pixel differences;
- visual regression methodology;
- accessibility checks;
- iterative fix → recapture → compare loop;
- objective completion criteria.

Red flags: one screenshot at one viewport, subjective "looks good" verification, no reference fidelity checks.

## 8. Product design / UX

Inspect:
- user/job framing;
- task-flow and state coverage;
- hierarchy and information architecture;
- accessibility;
- interaction costs and error recovery;
- research/evidence separation;
- design-system consistency;
- usability validation.

Red flags: visual polish without task-flow reasoning, invented research, no edge/error states.

## 9. Research

Inspect:
- source quality hierarchy;
- primary-source preference;
- citation/evidence discipline;
- date/freshness handling;
- contradiction resolution;
- uncertainty labeling;
- reproducible search strategy;
- separation of fact, claim, inference, and speculation.

Red flags: search snippets as evidence, fabricated citations, no freshness logic, confirmation bias.

## 10. Writing / communication

Inspect:
- audience and goal identification;
- preservation of source facts/constraints;
- tone and format control;
- structural editing versus surface polishing;
- factuality checks;
- revision criteria;
- avoidance of generic AI voice.

Red flags: style-only guidance, invented facts, no audience adaptation, destructive loss of source meaning.

## 11. Data analysis

Inspect:
- schema/data validation;
- missingness/outlier handling;
- reproducibility;
- correct statistical assumptions;
- leakage/confounding awareness;
- uncertainty and sensitivity analysis;
- traceable transformations;
- visualization appropriateness.

Red flags: inference from correlation without caveat, hidden data cleaning, no validation, p-value cargo culting.

## 12. Business workflows

Inspect:
- objective and decision linkage;
- measurable outputs;
- process boundaries;
- exception/escalation handling;
- auditability;
- permissions and human approval points;
- integration constraints;
- ROI/value measurement where relevant.

Red flags: vague "AI automation" claims, no process ownership, no exception path, no measurable success definition.

## 13. Agent-skill runtime / Claude Code

When Claude Code support is part of the promise or target use case, inspect:
- activation description quality and realistic over/under-trigger risk;
- project `.claude/skills/` versus personal `~/.claude/skills/` placement and intended sharing scope;
- invocation controls such as `disable-model-invocation` when automatic activation would be unsafe or noisy;
- `context: fork` only when isolated subagent execution fits an actionable task;
- `allowed-tools` / permission scoping for tool-using or externally impactful workflows;
- `${CLAUDE_SKILL_DIR}` or equivalent portable paths instead of fragile current-directory assumptions;
- plugin packaging under a plugin `skills/` directory when distribution is claimed;
- interaction with `CLAUDE.md`: CLAUDE.md is always-on context while skill bodies load on demand, so avoid duplicated large instructions;
- progressive disclosure because loaded skill content remains in context after invocation;
- trigger tests containing both should-trigger cases and adjacent near-miss should-not-trigger cases.

Do not penalize a purely portable Agent Skills implementation for omitting Claude-specific extensions it does not claim to support.

## 14. Unknown/new domains

Derive a lightweight overlay by asking:
1. What expert failure modes are common in this domain?
2. What evidence constitutes correctness?
3. What steps can be deterministic?
4. Which decisions require specialist judgment?
5. What safety/legal constraints matter?
6. What would a general frontier model likely miss?

Use the answers to interpret Domain expertise, Workflow, Verification, Safety, and Capability uplift. Do not invent formal standards you cannot verify.
