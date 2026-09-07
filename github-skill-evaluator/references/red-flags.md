# Red Flags and Quality Caps

## Table of contents

1. Content and methodology
2. Portability and dependencies
3. Safety and integrity
4. Evidence manipulation
5. Capability redundancy
6. Tier caps

## 1. Content and methodology

Flag when material:
- README-driven hype unsupported by implementation;
- generic LLM-generated advice presented as expertise;
- excessive verbosity or prompt bloat;
- contradictory instructions;
- cargo-cult architecture/pattern mandates;
- vague success criteria;
- no verification for outputs that are objectively verifiable;
- many examples that do not exercise failure modes;
- complexity added without behavioral benefit.

## 2. Portability and dependencies

Flag:
- hard-coded repository paths;
- assumptions about one project structure without declaring them;
- private tools/infrastructure required but undocumented;
- hidden environment variables;
- unavailable MCP/tool dependencies;
- unnecessary vendor lock-in;
- fragile shell/platform assumptions;
- dependencies with disproportionate installation or supply-chain cost.

Specialization is not itself a defect. Penalize only unjustified or hidden coupling.

## 3. Safety and integrity

Flag strongly:
- destructive commands without confirmation, scope check, backup, or rollback where appropriate;
- secret exfiltration or unsafe logging;
- arbitrary remote execution/download-and-run behavior without validation;
- broad permission requests not justified by task;
- silent destructive side effects;
- instructions to bypass security controls;
- functionally broken critical paths;
- deceptive behavior;
- copied material with unclear provenance when reuse rights matter;
- license missing or incompatible with intended reuse.

## 4. Evidence manipulation

Flag:
- stars/forks used as proof of correctness;
- screenshots presented as benchmarks;
- cherry-picked success examples;
- claims of production use with no supporting evidence;
- benchmark numbers without method/data/version;
- tests that merely assert implementation details rather than claimed behavior.

## 5. Capability redundancy

Flag low marginal value when the skill primarily says:
- write clean code;
- follow best practices;
- use SOLID;
- make the UI polished;
- test your work;
- think step-by-step/carefully;
- use meaningful names;
- handle errors.

These may be useful as part of a concrete workflow, but do not count them as expert uplift by themselves.

## 6. Tier caps

Apply judgment, but use these default caps:

| Condition | Default maximum tier |
|---|---|
| Critical destructive behavior without adequate safeguards | D |
| Malicious/deceptive behavior or clearly broken primary function | F |
| Required private/unavailable dependency is hidden/undocumented and blocks reuse | C |
| Material unresolved secret-exposure / arbitrary remote execution path | D or F depending on severity |
| No license for intended open-source reuse | No automatic cap; flag legal uncertainty and reduce fit/reusability if material |
| No tests/evals | No automatic cap; reduce Evidence/Verification only to degree justified by domain and claims |
| Low GitHub activity | No automatic cap |
| Low stars | Never a cap |

Explain every cap in the verdict.
