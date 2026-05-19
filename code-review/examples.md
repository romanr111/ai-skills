# Code Review Skill Examples

These examples calibrate output. Do not copy them blindly; adapt to the actual task, project rules, and evidence.

## Example 1 — clean Standard approval

```markdown
## Summary
The change matches the stated task and keeps the implementation small. Project gates passed, and I found no correctness, security, or test issues worth reporting.

## Verdict
**Approve**

## Validation run
- `npm test` — passed
- `npm run typecheck` — passed

No findings.
```

Why this is good:
- It does not manufacture comments.
- It states what was checked.
- It exits quickly when the code is fit for purpose.

## Example 2 — blocking task mismatch

```markdown
## Summary
The implementation handles CSV export but does not implement the requested versioned JSON backup format. This misses the core task requirement, so downstream style concerns are secondary.

## Verdict
**Reject (blocking)**

## Validation run
- `swift test` — passed

## Task-alignment findings
- [BLOCKING] Requested backup format is not implemented — `BackupService.export()` still writes CSV rows instead of the required `format/version/createdAt/...` JSON object — users cannot export wallets/categories/labels/relationships safely, which was the main purpose of the task — add a versioned JSON export model and write the full backup payload before keeping CSV as a separate export path.
```

Why this is good:
- The finding maps directly to the requirement.
- The consequence is product-level, not stylistic.
- The fix is minimal and specific.

## Example 3 — security finding

```markdown
## Correctness / security findings
- [BLOCKING] User-controlled path can escape the export directory — `ExportController.save(fileName:)` joins `baseDir + fileName` without normalizing and checking containment — a filename like `../../Documents/private.json` can overwrite files outside the intended folder — resolve the path, reject traversal, and verify the final path remains under the export directory before writing.
```

Why this is good:
- It names the exploit path.
- It avoids vague "this is unsafe" language.
- It gives the smallest fix.

## Example 4 — test gap that matters

```markdown
## Tests
- [IMPORTANT] No test covers duplicate transaction import idempotency — `BankSyncServiceTests` only verifies a new transaction is inserted once — the task requires existing history not to be rewritten, so a regression could duplicate or mutate existing expenses silently — add a test where the same bank transaction is synced twice and assert the existing local transaction remains unchanged.
```

Why this is good:
- It does not ask for generic “more tests.”
- It ties the test gap to an explicit requirement.

## Example 5 — overengineering false positive to avoid

Do not write this:

```markdown
- [SUGGESTION] Consider introducing an `Exporter` protocol and dependency injection container for backup export.
```

If the current code is one simple export function and there is only one export implementation, this is likely reviewer-created YAGNI.

Better, if there is no concrete problem:

```markdown
No maintainability findings. The single export function is appropriate for the current scope.
```

## Example 6 — declared gate failure

```markdown
## Summary
The implementation appears directionally aligned with the task, but the declared typecheck gate fails. This must be fixed before merge.

## Verdict
**Reject (blocking)**

## Validation run
- `pnpm typecheck` — failed: `src/sync/mapper.ts:42:17 - Type 'string | undefined' is not assignable to type 'string'`
- `pnpm test` — not run because typecheck failed first

## Correctness / security findings
- [BLOCKING] Declared typecheck gate fails — `mapper.ts:42` passes an optional external transaction ID into a required local ID field — this can create records without stable deduplication keys — validate the ID before mapping or generate a local stable key for missing external IDs.
```

Why this is good:
- It reports exact command and failure.
- It links the tooling failure to a real consequence.

## Example 7 — Detailed review with partial verification

```markdown
## Summary
Detailed review found no task-alignment blocker, but validation is incomplete because the integration test environment is unavailable. The main remaining risk is migration compatibility during rolling deploy.

## Verdict
**Request changes**

## Validation run
- `go test ./...` — passed
- `make integration-test` — not run: requires local Postgres fixture not present in this environment

## Correctness / security findings
- [IMPORTANT] Migration is not backward-compatible with the currently deployed app version — `003_add_required_status.sql` adds `status TEXT NOT NULL` without a default while older app instances still insert rows without `status` — rolling deploy can fail writes during the deployment window — deploy in two steps: add nullable/defaulted column first, backfill, update app, then enforce `NOT NULL` in a later migration.
```

Why this is good:
- It is honest about what was not verified.
- It focuses on a deployment-realistic failure mode.
