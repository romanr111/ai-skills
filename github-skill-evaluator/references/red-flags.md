# Red Flags and Quality Caps

Flag only material issues.

## Content and methodology
- README-driven hype unsupported by implementation
- generic LLM advice presented as expertise
- excessive verbosity/prompt bloat
- contradictory instructions
- cargo-cult patterns
- vague success criteria
- objectively verifiable outputs with no verification
- complexity without behavioral benefit

## Evidence integrity
- scoring a dimension without an inspected evidence path
- stars/forks used as correctness evidence
- screenshots presented as benchmarks
- benchmark numbers without metric/baseline/method/repetition
- tests/evals that do not measure the promised outcome
- cherry-picked examples presented as general effectiveness
- `strong` or `exceptional` capability uplift claimed without the required baseline probe

## Portability and dependencies
- hard-coded repository paths
- hidden environment variables/private infrastructure
- unavailable MCP/tool dependencies
- unnecessary vendor lock-in
- fragile platform assumptions
- disproportionate install/supply-chain cost

Specialization itself is not a defect.

## Safety and integrity
- destructive commands without adequate confirmation/scope/rollback
- secret exfiltration or unsafe logging
- arbitrary remote execution/download-and-run without validation
- broad permissions unjustified by task
- silent destructive side effects
- bypassing security controls
- broken primary function
- deceptive behavior
- copied material with unclear provenance
- unclear/incompatible license for intended reuse

## Capability redundancy
Low marginal value if the skill mainly says:
- write clean code
- follow best practices
- use SOLID
- make UI polished
- test your work
- think carefully
- use meaningful names
- handle errors

These can support a concrete workflow but are not expert uplift by themselves.

## Tier caps

| Condition | Default maximum tier |
|---|---|
| Critical destructive behavior without adequate safeguards | D |
| Malicious/deceptive behavior or clearly broken primary function | F |
| Hidden required private/unavailable dependency blocks reuse | C |
| Material unresolved secret exposure / arbitrary remote execution | D or F |
| No clear license for intended open-source reuse | no automatic cap; flag and reduce reuse/fit when material |
| No tests/evals | no automatic cap; reduce only relevant evidence/verification bands |
| Low activity | no automatic cap |
| Low stars | never a cap |

Explain every cap.
