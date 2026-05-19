---
name: pr-description
description: >
  Concise pull request title and description generator. Use when the user asks
  to write, rewrite, tighten, draft, or improve a PR/MR description, pull
  request body, merge request body, PR title, or invokes /pr-description.
  Optimized for terse, reviewer-useful descriptions that preserve intent,
  reasoning, validation, risks, and follow-up context without filler.
---

Write PR descriptions terse and exact. Reviewer value over changelog noise. Why over what.

## Rules

**First gather evidence when possible:**
- Prefer the actual diff, commits, issue text, existing PR body, CI results, and user request.
- If evidence is missing, say what is unknown instead of inventing scope or validation.
- Do not inspect or print secrets.

**Title:**
- Imperative or noun phrase, matching project convention.
- Aim for 50 characters; hard cap 72 when practical.
- No trailing period.
- Mention the user-visible behavior or system area, not file churn.

**Body:**
- Default format:
  ```
  ## Summary
  - ...

  ## Testing
  - ...
  ```
- If the repository has a PR template, preserve its headings and order; fill it tersely instead of replacing it.
- Add only useful extra sections:
  - `## Why` for non-obvious motivation or product context.
  - `## Risk` for migrations, security, data loss, auth, billing, compatibility, or rollout hazards.
  - `## Notes` for reviewer-specific context or deliberate non-goals.
  - `Closes #123` / `Refs #123` at the end when known.
- Keep bullets short. One fact per bullet.
- Put validation under `Testing`, including commands, CI jobs, manual checks, or `Not run (...)`.
- If nothing was tested, write `- Not run (reason).`

**What NEVER goes in:**
- "This PR", "I", "we", "now", "currently", "just", "simply", "basically".
- AI attribution or generator signatures.
- Diff narration that repeats file names without explaining behavior.
- Speculative benefits, unverified performance claims, or hidden uncertainty.
- Large pasted logs. Summarize and cite the exact command/job instead.

## Auto-Clarity

Always include enough context for breaking changes, security fixes, data migrations,
permission changes, dependency upgrades, rollbacks, and behavior that ordinary users
could misread from a terse summary.

Do not compress away:
- migration order
- compatibility impact
- user-visible behavior
- rollback notes
- validation caveats

## Examples

Small fix:
```
Title: fix CSV import from document providers

## Summary
- Preserve security-scoped file access while reading selected CSVs.
- Keep existing parsing and validation behavior unchanged.

## Testing
- `swift test`
- Manual import from iCloud Drive on device.
```

Risky change:
```
Title: rename checkout order API

## Summary
- Move checkout creation from `/v1/orders` to `/v1/checkout`.
- Return `410 Gone` from the old route after the migration window.

## Risk
- Breaking API change for clients still calling `/v1/orders`.
- Clients must migrate before 2026-06-01.

## Testing
- `npm test`
- Contract test for old route deprecation response.

Closes #128
```

## Boundaries

Only writes or rewrites PR title/body text. Does not create PRs, push branches,
stage files, commit changes, or edit repository files unless the user explicitly
asks for those actions. Output the result as paste-ready Markdown unless the user
requests a direct GitHub update.
