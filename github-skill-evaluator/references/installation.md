# Installation

The portable unit is the entire `github-skill-evaluator/` directory. `SKILL.md` uses only the required cross-platform frontmatter fields (`name`, `description`).

## Claude Code

Project-local:

```bash
mkdir -p .claude/skills
cp -R /path/to/github-skill-evaluator .claude/skills/github-skill-evaluator
```

Personal:

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/github-skill-evaluator ~/.claude/skills/github-skill-evaluator
```

Claude Code currently discovers project skills from `.claude/skills/<skill-name>/SKILL.md` and personal skills from `~/.claude/skills/<skill-name>/SKILL.md`.

## OpenAI Codex

Prefer the cross-agent Agent Skills locations used by current Codex discovery.

Repository/project:

```bash
mkdir -p .agents/skills
cp -R /path/to/github-skill-evaluator .agents/skills/github-skill-evaluator
```

Personal/global:

```bash
mkdir -p ~/.agents/skills
cp -R /path/to/github-skill-evaluator ~/.agents/skills/github-skill-evaluator
```

`$CODEX_HOME/skills` (commonly `~/.codex/skills`) remains a legacy/backward-compatible location in current Codex implementations, but it should not be presented as the preferred portable location for new skills.

The optional `agents/openai.yaml` provides Codex-specific UI metadata where supported; it does not change the portable Agent Skills core behavior.

## Generic Agent Skills environments

For tools that discover repository skills under `.agents/skills/`:

```bash
mkdir -p .agents/skills
cp -R /path/to/github-skill-evaluator .agents/skills/github-skill-evaluator
```

## One canonical copy

Prefer a real directory or copied skill when interoperability matters. Some agent implementations have had discovery limitations around symlinked skill roots. If you use symlinks, verify discovery in the target client rather than assuming it works.
