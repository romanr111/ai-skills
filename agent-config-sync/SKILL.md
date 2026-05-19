# Agent Config Sync

Synchronize global agent configuration (AGENTS.md and custom skills) across all installed coding agents, using one agent as the baseline source of truth.

## Overview

This skill keeps your cross-agent configuration strictly consistent. Pick any agent as the baseline; every other agent gets overwritten to match it.

Supported agents:
- **Codex**: `~/.codex/AGENTS.md` + `~/.codex/skills/`
- **Opencode**: `~/.config/opencode/AGENTS.md` + `~/.opencode/skills/`
- **Kimi**: `~/.kimi/AGENTS.md` + `~/.kimi/skills/`

## Usage

### Interactive (recommended)

```bash
# Preview changes from default baseline (codex)
python ~/.codex/skills/agent-config-sync/scripts/sync.py

# Preview changes from a different baseline
python ~/.codex/skills/agent-config-sync/scripts/sync.py --baseline kimi

# Apply changes
python ~/.codex/skills/agent-config-sync/scripts/sync.py --yes
python ~/.codex/skills/agent-config-sync/scripts/sync.py --baseline opencode --yes
```

## What gets synchronized

1. **AGENTS.md** — global system prompt / behavioral rules
   - Copied from the baseline to every other agent.
   - Agent-specific paths (e.g., `/Users/roman/.codex/...`) are automatically rewritten to match each target agent's home directory.

2. **Custom skills** — reusable capabilities under `skills/`
   - Copied from the baseline to every other agent.
   - **Existing skills are overwritten** if they differ from the baseline.
   - **Extra files in target skills** (not present in baseline) are removed.
   - Hidden/system directories (`.system`, `.DS_Store`, `.tmp`, `__pycache__`) are ignored.

## Safety

- The script performs a **dry-run by default** unless `--yes` is passed.
- The baseline agent is never modified.
- AGENTS.md is always overwritten to maintain strict alignment.
- Skills are fully overwritten to ensure exact mirroring of the baseline.
