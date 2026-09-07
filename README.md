# AI Skills

A collection of custom skills for AI coding agents (Kimi, Claude, Codex, etc.).

## Skills

| Skill | Description |
|-------|-------------|
| [`agent-config-sync`](./agent-config-sync) | Sync agent configuration across projects |
| [`caveman-compress`](./caveman-compress) | Compress natural language memory files into concise formats |
| [`code-review`](./code-review) | Language-neutral code review workflow for PRs and changes |
| [`github-skill-evaluator`](./github-skill-evaluator) | Discover, evidence-check, compare, and rank reusable open-source Agent Skills |
| [`pr-description`](./pr-description) | Generate concise, reviewer-useful PR titles and descriptions |
| [`tdd`](./tdd) | Test-driven development workflow and patterns |

## Usage

The skills use `SKILL.md` entry points and are intended to be portable across skill-capable agents. Some older skills were originally shaped around Kimi CLI conventions; inspect each skill's metadata and installation notes for agent-specific features.

To use with **Kimi CLI**:

```bash
# Symlink or copy into your user skills directory
ln -s $(pwd)/code-review ~/.kimi/skills/code-review
ln -s $(pwd)/tdd ~/.kimi/skills/tdd
```

For Claude Code, Codex, and other Agent Skills-compatible environments, copy or symlink the relevant skill directory into the agent's supported skill location. Agent-specific metadata such as `agents/openai.yaml` is optional and does not replace the portable `SKILL.md` core.

## License

MIT — see [LICENSE](./LICENSE).
