# AI Skills

A collection of custom skills for AI coding agents (Kimi, Claude, Codex, etc.).

## Skills

| Skill | Description |
|-------|-------------|
| [`agent-config-sync`](./agent-config-sync) | Sync agent configuration across projects |
| [`caveman-compress`](./caveman-compress) | Compress natural language memory files into concise formats |
| [`code-review`](./code-review) | Language-neutral code review workflow for PRs and changes |
| [`github-skill-evaluator`](./github-skill-evaluator) | Evidence-first evaluation, comparison, and ranking of open-source Agent Skills |
| [`pr-description`](./pr-description) | Generate concise, reviewer-useful PR titles and descriptions |
| [`tdd`](./tdd) | Test-driven development workflow and patterns |

## Usage

These skills follow the [Kimi CLI skill format](https://docs.kimi.ai/skills), but are generally portable to any agent system that reads `SKILL.md` files.

To use with **Kimi CLI**:

```bash
# Symlink or copy into your user skills directory
ln -s $(pwd)/code-review ~/.kimi/skills/code-review
ln -s $(pwd)/tdd ~/.kimi/skills/tdd
```

To use with **Claude / other agents**:
Reference the `SKILL.md` file directly in your prompt or system instructions.

## License

These are personal/custom skills. Use and modify as needed.
