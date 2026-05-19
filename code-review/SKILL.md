---
name: code-review
version: 2
summary: Efficient language-neutral code review skill for coding agents.
description: Use this for code review, PR/MR review, implementation checks, and merge-readiness. Review changes in any language. Default to Standard review; use Detailed review only when requested or when risk is high. Verify task alignment first, discover project gates, and report only high-confidence findings with concrete consequences.
---

# Code Review Skill

Use this skill whenever the user asks for a code review, PR/MR review, implementation check, "is this good?", "look this over", "check my changes", or asks whether code is ready to merge.

The goal is not to produce many comments. The goal is to decide whether the change is fit for purpose, safe to merge, and aligned with the original task.

## Review complexity

There are only two review levels.

### 1. Standard review — default

Use unless the user explicitly asks for deeper review or the change is clearly high-risk.

Focus:
- task alignment
- correctness bugs
- security risks
- broken project gates
- test adequacy for the change
- maintainability issues with concrete consequences
- obvious performance problems on realistic data paths

Do not perform broad architecture review unless the diff changes architecture-relevant boundaries.

### 2. Detailed review

Use when the user asks for deep/detailed/strict review, asks for self-review, or the change touches high-risk areas:
- auth, permissions, secrets, payments, finance, medical, personal data, crypto, deployment, migrations, concurrency, data loss, public APIs, backup/restore, import/export, or irreversible operations
- large multi-file refactors
- production-readiness assessment
- before merging a critical PR

Detailed review adds:
- deeper edge-case analysis
- threat-model thinking where relevant
- API/domain design review
- concurrency/lifecycle review
- migration/backward-compatibility review
- more complete test-gap analysis
- broader caller/integration inspection

## Prime directive — fit for purpose, not elaborate

A review must match the size and risk of the change.

- A small correct function/script is finished. Do not ask for classes, interfaces, dependency injection, framework layers, plugin systems, or config abstractions unless there is a concrete need.
- Prefer the smallest design that satisfies the task.
- A function, closure, value type, or module-level helper is a valid abstraction.
- Do not propose architecture rewrites unless the current design directly causes a bug, security gap, hard-to-test boundary, real duplication, or likely maintenance failure.
- Drop comments based only on taste, naming preference, line layout, or personal style unless project rules require them.

This directive overrides all other principles when they would add ceremony without solving a concrete problem.

## Operating mode

First classify the user's intent:

- **review-only**: inspect and report. Do not edit files.
- **review-and-fix**: review, then apply minimal safe fixes if the user asked you to fix.
- **fix-then-review**: implement requested change, then review your own change before final response.

If the user only asks for a review, default to review-only.

## Safety rules for coding agents

Do not run destructive or externally impactful commands unless the user explicitly requested them and the risk is understood:

- `rm -rf`, broad delete commands, or deleting user data
- `git reset --hard`, `git clean -fdx`, force push, history rewrite
- production deploys, publishing packages, submitting apps
- database migrations against non-local databases
- commands that print secrets or dump `.env` values
- network actions that mutate external systems

Prefer read-only commands for review. If a command may write, skip it or explain why it was not run.

Never claim a command passed unless you actually ran it and observed success.

## Workflow

### Step 1 — establish task and scope

Anchor the review on the intended task before judging code.

Look for the task in this order:
1. user-provided task/spec in the conversation
2. PR/MR description or linked issue
3. commit messages on the branch
4. ticket/design doc referenced by the user
5. nearby project documentation

If no meaningful task can be found, say that task alignment cannot be verified. In review-only mode, still review for obvious correctness/security/test issues instead of inventing requirements.

Determine the diff:
- default: staged + unstaged changes against `HEAD`
- PR/MR: diff against merge base, for example `git diff <base>...HEAD`
- named files: restrict to those files

Read full changed files, not only hunks. For Standard review, read direct callers/tests when needed. For Detailed review, also inspect integration boundaries affected by the change.

### Step 2 — load project rules

Before applying general preferences, inspect project-specific instructions and conventions:

- `AGENTS.md`, `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`
- CI files: `.github/workflows/*`, GitLab CI, Azure Pipelines, CircleCI
- build/test/lint config: package manager scripts, `Makefile`, `justfile`, `Taskfile`, language config files
- nearby code style and test patterns

Project rules beat general rules unless they create a concrete bug, security issue, or explicit task mismatch.

### Step 3 — discover validation gates

Discover gates from the project, do not assume them.

Check in this order:
1. CI workflow commands
2. `package.json` scripts, `Makefile`, `justfile`, `Taskfile`, or equivalent
3. language/build configuration
4. README/CONTRIBUTING instructions
5. ecosystem defaults only if no project command exists

Run the narrowest reliable read-only gate set appropriate to the change:
- format/check-only gate if available
- lint/static analysis
- type check or compiler check
- relevant tests
- build if the change affects build/package/runtime integration

If no declared gates exist, state: `No project-declared validation gates found.` Then continue manual review.

If dependencies are unavailable or commands cannot run, report exactly what could not be run and why. Do not convert unavailable tooling into a code finding.

### Step 4 — review in priority order

Review in this order. Findings from earlier layers dominate later ones.

1. **Task alignment**
   - Does the implementation satisfy each explicit requirement?
   - Does it solve the right problem, not an adjacent easier one?
   - Are acceptance criteria and named edge cases covered?
   - Is there unrelated scope creep?
   - Are there TODOs, stubs, mocks, or hard-coded behavior where production behavior was required?

2. **Correctness**
   - realistic runtime failures
   - invalid state handling
   - boundary cases
   - data consistency
   - lifecycle/order-of-operation bugs
   - compatibility with existing callers

3. **Security and data safety**
   - injection, authz/authn, secrets, path traversal, unsafe deserialization, unsafe shelling out
   - privacy leaks, logging sensitive data
   - irreversible data loss or corrupt backup/restore behavior

4. **Tests**
   - tests cover behavior, not implementation details
   - task requirements and important edge cases are tested
   - tests are deterministic and do not depend on real network/time/global state unless intentionally integrated
   - mocks represent real dependency behavior

5. **Maintainability and principles**
   - DRY: duplicated business knowledge, not incidental similarity
   - KISS: avoid cleverness and hidden control flow
   - YAGNI: avoid speculative abstractions/configuration
   - SoC: separate domain logic from I/O/framework/rendering when it matters
   - Fail Fast: validate invalid state at boundaries
   - SOLID/OOP: apply only when classes/interfaces are actually warranted

6. **Performance**
   - flag only realistic hot-path or scale issues
   - prefer simple O(n) fixes over elaborate caching unless caching is clearly needed

7. **Language-specific craft**
   - load the relevant section from `language-profiles.md` only for languages touched by the diff
   - do not report language-style issues unless they affect correctness, safety, maintainability, or project rules

### Step 5 — finding contract

Only report findings with confidence >= 70/100.

Every finding must include:
- severity: `BLOCKING`, `IMPORTANT`, or `SUGGESTION`
- evidence: file/line/function or exact behavior
- consequence: what can break, leak, regress, or become costly
- principle/category: task alignment, correctness, security, tests, DRY, KISS, etc.
- minimal fix: the smallest concrete fix that resolves the problem

Severity calibration:

- **BLOCKING**: task requirement not met, realistic runtime failure, exploitable security/data-loss issue, broken declared gate, migration/compatibility break, or production-critical test gap.
- **IMPORTANT**: clear correctness/maintainability/test issue with concrete cost, but not necessarily merge-blocking in all contexts.
- **SUGGESTION**: useful improvement, safe to ignore without breaking the task.

Do not report:
- pure preference
- trivia a formatter handles
- renaming without consequence
- adding abstractions/classes/helpers used once
- docstring requests for trivial private helpers
- duplicate restatement of linter output unless it affects verdict

If no findings survive this filter, approve plainly.

### Step 6 — self-review before final response

Before emitting the review, challenge every finding:

1. Did I verify the cited code actually exists?
2. Is the consequence concrete?
3. Is the severity honest?
4. Is the finding based on the task/project rules rather than taste?
5. Am I over-engineering a small correct change?
6. Am I duplicating tooling output unnecessarily?
7. Does the verdict match the findings?

Drop weak findings. A short approval is better than padded noise.

## Output format

Use this structure. Omit empty sections.

```markdown
## Summary
<1-3 sentences. State task alignment, gate status, and whether blockers exist.>

## Verdict
**Approve** | **Approve with comments** | **Request changes** | **Reject (blocking)**

## Validation run
- `<command>` — passed/failed/not run: <reason or key output>

## Task-alignment findings
- [severity] <finding> — <evidence> — <consequence> — <minimal fix>

## Correctness / security findings
- [severity] <finding> — <evidence> — <consequence> — <minimal fix>

## Tests
- [severity] <finding> — <evidence> — <consequence> — <minimal fix>

## Maintainability / principles
- [severity] [principle] <finding> — <evidence> — <consequence> — <minimal fix>

## Nice-to-haves / follow-ups
- <optional non-blocking item>
```

Verdict rules:
- **Approve**: no findings, or only negligible notes not worth listing.
- **Approve with comments**: suggestions or minor important issues that do not block merge.
- **Request changes**: at least one important issue should be fixed before merge.
- **Reject (blocking)**: at least one blocking issue exists.

## Agent efficiency rules

For Standard review:
- inspect changed files, relevant tests, direct callers, and project gates
- avoid broad repo-wide exploration unless the diff crosses boundaries
- prefer one concise final report

For Detailed review:
- inspect integration points and failure modes more broadly
- group findings by risk, not by file order
- explicitly state what could not be verified

When fixing is requested:
- make the smallest patch that resolves the finding
- do not refactor unrelated code
- run relevant gates after patching
- final response must distinguish fixed issues from remaining risks
