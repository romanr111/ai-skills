# Language Profiles for Code Review

Load only the sections relevant to the files changed. These are checklists, not automatic findings. Report an item only when it creates a concrete correctness, security, performance, testability, or maintainability consequence.

## Python

High-signal checks:
- mutable default arguments
- broad `except Exception` / bare `except` without re-raise or clear recovery
- `assert` used for runtime validation
- naive UTC datetimes where aware datetimes are required
- blocking I/O inside `async def`
- untrusted `eval`, `exec`, `pickle`, unsafe YAML load
- shell command construction with interpolated user input
- SQL string interpolation instead of parameters
- path traversal via unvalidated user paths
- tests coupled to real time, network, global state, or implementation internals

Common gates:
- project-declared `pytest`, `ruff`, `mypy`, `pyright`, `pyre`, `tox`, `nox`, or `pre-commit`

## JavaScript / TypeScript

High-signal checks:
- `any` leakage across public boundaries without justification
- unchecked `null` / `undefined` where `strictNullChecks` is enabled or expected
- missing `await`, unhandled promises, fire-and-forget without lifecycle handling
- swallowed errors in `catch`
- unsafe object indexing or prototype pollution risks
- unsafe DOM insertion / XSS risks
- secrets exposed to client bundles
- server/client boundary violations in full-stack frameworks
- tests that only mock the implementation under test

Common gates:
- project-declared `test`, `lint`, `typecheck`, `build`, `format:check`, `biome`, `eslint`, `tsc --noEmit`, framework-specific checks

## Swift / iOS

High-signal checks:
- UI updates off the main actor/thread
- retain cycles in closures, delegates, timers, Combine subscriptions, async tasks
- missing cancellation for async work tied to view lifecycle
- unstable SwiftUI identity causing state loss or performance regressions
- expensive work in view body/render path
- force unwraps on realistic nil paths
- persistence migrations or model changes without compatibility plan
- background task, permission, keychain, file protection, or privacy misuse
- tests missing for domain logic separated from UI

Common gates:
- project-declared `xcodebuild test`, `swift test`, SwiftLint, SwiftFormat check, build scheme checks

## Go

High-signal checks:
- ignored errors
- context not propagated to I/O, database, HTTP, or goroutines
- goroutine leaks or channels that can block forever
- data races on shared state
- nil pointer paths
- misuse of `defer` in hot loops
- non-deterministic tests due to time/network/global state
- table tests missing important boundary cases

Common gates:
- `go test ./...`, `go test -race ./...` when relevant, `go vet ./...`, `gofmt` check via `test -z "$(gofmt -l .)"`

## Rust

High-signal checks:
- `unwrap` / `expect` on realistic failure paths outside tests/prototypes
- panic across library/public API boundaries
- incorrect ownership/lifetime workaround that hides design issue
- unsafe blocks without local invariant explanation
- error types that discard actionable context
- async tasks without cancellation/backpressure where relevant
- clone-heavy code on hot paths without need

Common gates:
- `cargo test`, `cargo clippy -- -D warnings`, `cargo fmt --check`, feature-specific build/test commands

## Java / Kotlin

High-signal checks:
- nullability contract violations
- resource leaks: streams, files, DB handles, HTTP responses
- blocking calls on UI/event-loop/reactive threads
- swallowed exceptions or logged-and-continued invalid state
- transaction boundary bugs
- framework lifecycle misuse
- excessive inheritance where composition is simpler
- tests that require real external services without isolation

Common gates:
- Gradle/Maven test, check, lint, detekt/ktlint, compile tasks, framework-specific integration checks

## C# / .NET

High-signal checks:
- `async void` outside event handlers
- missing `CancellationToken` propagation for cancellable I/O
- undisposed `IDisposable` / `IAsyncDisposable`
- sync-over-async deadlocks
- nullable reference type violations
- LINQ causing repeated enumeration or hidden O(n²) behavior
- incorrect DI lifetime: singleton capturing scoped/transient state
- EF query materialization too early or N+1 queries

Common gates:
- `dotnet test`, `dotnet build`, analyzers, format check if configured

## SQL / database migrations

High-signal checks:
- destructive migration without backup/rollback/compatibility plan
- non-idempotent migration where deployment may retry
- missing indexes for newly introduced query patterns
- transaction boundary and partial-write failures
- SQL injection risks
- migration incompatible with zero-downtime rollout
- app code and schema changes not backward-compatible during deployment window

Common gates:
- migration dry-run/status commands, project-specific integration tests, SQL lint if configured

## Shell / Bash / Zsh

High-signal checks:
- unquoted variables leading to word splitting/globbing
- unsafe `rm`, broad globs, or destructive defaults
- missing `set -euo pipefail` in scripts where fail-fast is intended
- command injection via interpolated user input
- reliance on current working directory without validation
- non-portable shell assumptions when script claims portability
- secrets printed to logs

Common gates:
- shellcheck if configured, dry-run mode if available, targeted execution on safe sample inputs

## C / C++

High-signal checks:
- memory ownership ambiguity, leaks, double free, use-after-free
- buffer overflows or unchecked lengths
- undefined behavior: signed overflow, invalid casts, lifetime issues
- missing RAII in C++ where available
- thread-safety and data races
- exception-safety around resource ownership
- ABI/API compatibility breaks

Common gates:
- project build, unit tests, sanitizers when configured, clang-tidy/cppcheck if configured

## Web / frontend UI

Use in addition to the language profile.

High-signal checks:
- state updates causing render loops or stale closures
- accessibility regressions for interactive controls
- hydration/server-client mismatch
- layout shift or expensive rendering in large lists
- unsafe HTML injection
- broken loading/error/empty states
- tests missing for critical user flows

## Mobile / desktop app UI

Use in addition to Swift/Kotlin/C#/TypeScript profile when relevant.

High-signal checks:
- main-thread blocking and scroll/tap performance issues
- lifecycle leaks: observers, subscriptions, timers, tasks
- offline/error states
- persistence consistency during app termination/backgrounding
- permission prompts without clear user action
- platform design convention violations that harm usability
