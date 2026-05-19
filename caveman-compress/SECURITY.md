# Security

## Snyk High Risk Rating

`caveman-compress` receives a Snyk High Risk rating due to static analysis heuristics. This document explains what the skill does and does not do.

### What triggers the rating

1. **subprocess usage**: The skill can call model CLIs (`codex`, `opencode`, `claude`, or `CAVEMAN_LLM_COMMAND`) via `subprocess.run()`. Built-in provider calls use fixed argument lists — no shell interpolation occurs. User file content is passed via stdin, a temporary prompt file, or an argv value depending on provider.

2. **File read/write**: The skill reads the file the user explicitly points it at, compresses it, and writes the result back to the same path. A `.original.md` backup is saved alongside it. No files outside the user-specified path are read or written.

### What the skill does NOT do

- Does not execute user file content as code
- Does not make direct network requests except through the configured model provider
- Does not access files outside the path the user provides
- Does not use shell=True or string interpolation in subprocess calls
- Does not collect or transmit any data beyond the file being compressed

### Model provider behavior

Default provider is `auto`: `CAVEMAN_LLM_COMMAND`, then Anthropic SDK if `ANTHROPIC_API_KEY` is set, then installed `codex`, `opencode`, or `claude` CLIs. Set `CAVEMAN_PROVIDER=codex|opencode|claude|anthropic|auto` to force one provider. CLI providers use the user's existing local authentication.

### File size limit

Files larger than 500KB are rejected before any API call is made.

### Reporting a vulnerability

If you believe you've found a genuine security issue, please open a GitHub issue with the label `security`.
