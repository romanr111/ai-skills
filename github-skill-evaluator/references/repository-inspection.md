# Repository Inspection Protocol

## Table of contents

1. Define the evaluation unit
2. Inspection order
3. Depth parity for comparisons
4. Evidence ledger
5. GitHub/repository metadata
6. Stop conditions

## 1. Define the evaluation unit

Before scoring, identify what is actually being evaluated:
- one `SKILL.md` directory;
- a collection of related skills intended to work together;
- an entire skill repository/framework.

Score the named unit. Repository-wide license, maintenance, CI, and shared tooling may affect that unit, but unrelated sibling skills must not inflate its Domain expertise, Workflow, Verification, or Uplift scores.

When a repository has many skills, map only the target skill's direct dependencies and shared resources.

## 2. Inspection order

Prefer this order because it minimizes README anchoring:

1. target `SKILL.md`;
2. files directly referenced by it;
3. scripts/tools that implement claimed behavior;
4. tests/evals/fixtures tied to those behaviors;
5. realistic examples;
6. dependency/configuration files;
7. license and installation requirements;
8. CI/release metadata;
9. issues/PRs/commits when they answer a material question;
10. README/marketing claims and community signals.

README can be useful for orientation, but do not let it define the score before inspecting implementation.

## 3. Depth parity for comparisons

Inspect candidates to comparable **decision-relevant depth**, not identical file count.

For each candidate, obtain enough evidence to answer:
- what procedure does it add?
- what unique expertise does it encode?
- how is output verified?
- what dependencies/assumptions limit reuse?
- what evidence supports effectiveness?
- what are the material failure/safety modes?

If one candidate has inaccessible material components, mark the comparison asymmetric and lower confidence rather than filling the gap with assumptions.

## 4. Evidence ledger

Maintain a compact internal ledger while inspecting:

| Claim/dimension | Evidence | Label | Limitation |
|---|---|---|---|
| Verification loop exists | `SKILL.md` + test script | Repository evidence | Not executed locally |
| Improves defect rate | README statement | Author claim | No benchmark found |
| Portable across OSes | Python stdlib script, no shell dependency | Inference | Windows not tested |

Use the ledger to prevent claim laundering. A statement does not become verified merely because it appears repeatedly across README/examples.

## 5. GitHub/repository metadata

Use repository metadata only where relevant:

### Material primary/near-primary signals
- license;
- tagged releases/versioning if compatibility matters;
- commit history for maintenance risk;
- issues/PRs documenting real defects or adoption;
- CI status/tests;
- dependency updates/security fixes.

### Weak social signals
- stars;
- forks;
- watchers;
- contributor count;
- social mentions.

Do not spend substantial search effort collecting social metrics unless the user asks about adoption/community specifically.

## 6. Stop conditions

Stop inspecting when additional files are unlikely to change the decision. Do not recursively read a large repository for completeness theater.

Continue deeper when:
- a high-impact claim is unsupported;
- a referenced script determines core behavior;
- safety depends on implementation details;
- candidates are close enough that more evidence may change the ranking;
- license/dependency ambiguity affects reuse;
- tests/evals make strong effectiveness claims that need inspection.
