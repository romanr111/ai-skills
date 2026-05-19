<p align="center">
  <img src="https://em-content.zobj.net/source/apple/391/rock_1faa8.png" width="80" />
</p>

<h1 align="center">caveman-compress</h1>

<p align="center">
  <strong>shrink memory file. save token every session.</strong>
</p>

---

A Codex/OpenCode/Claude-compatible skill that compresses your project memory files (`AGENTS.md`, `CLAUDE.md`, `MEMORY.md`, todos, preferences) into caveman format — so every session loads fewer tokens automatically.

Agents read memory files on session start. If file big, cost big. Caveman make file small. Cost go down forever.

## What It Do

```
/caveman-compress MEMORY.md
```

```
MEMORY.md          ← compressed (agent reads this — fewer tokens every session)
MEMORY.original.md ← human-readable backup (you edit this)
```

Original never lost. You can read and edit `.original.md`. Run skill again to re-compress after edits.

## Benchmarks

Real results on real project files:

| File | Original | Compressed | Saved |
|------|----------:|----------:|------:|
| `claude-md-preferences.md` | 706 | 285 | **59.6%** |
| `project-notes.md` | 1145 | 535 | **53.3%** |
| `claude-md-project.md` | 1122 | 636 | **43.3%** |
| `todo-list.md` | 627 | 388 | **38.1%** |
| `mixed-with-code.md` | 888 | 560 | **36.9%** |
| **Average** | **898** | **481** | **46%** |

All validations passed ✅ — headings, code blocks, URLs, file paths preserved exactly.

## Before / After

<table>
<tr>
<td width="50%">

### 📄 Original (706 tokens)

> "I strongly prefer TypeScript with strict mode enabled for all new code. Please don't use `any` type unless there's genuinely no way around it, and if you do, leave a comment explaining the reasoning. I find that taking the time to properly type things catches a lot of bugs before they ever make it to runtime."

</td>
<td width="50%">

### 🪨 Caveman (285 tokens)

> "Prefer TypeScript strict mode always. No `any` unless unavoidable — comment why if used. Proper types catch bugs early."

</td>
</tr>
</table>

**Same instructions. 60% fewer tokens. Every. Single. Session.**

## Security

`caveman-compress` is flagged as Snyk High Risk due to subprocess and file I/O patterns detected by static analysis. This is a false positive — see [SECURITY.md](./SECURITY.md) for a full explanation of what the skill does and does not do.

## Install

Compress is built in with the `caveman` plugin. Install `caveman` once, then use `/caveman-compress`.

If you need local files, the compress skill lives at:

```bash
caveman-compress/
```

**Requires:** Python 3.10+

## Usage

```
/caveman-compress <filepath>
```

Examples:
```
/caveman-compress MEMORY.md
/caveman-compress docs/preferences.md
/caveman-compress todos.md
```

### Model provider

Default provider is `auto`:

1. `CAVEMAN_LLM_COMMAND` if set
2. Anthropic SDK if `ANTHROPIC_API_KEY` is set
3. `codex exec` if `codex` is installed
4. `opencode run` if `opencode` is installed
5. `claude --print` if `claude` is installed

Force a provider:

```bash
CAVEMAN_PROVIDER=codex python3 -m scripts /path/to/MEMORY.md
CAVEMAN_PROVIDER=opencode python3 -m scripts /path/to/MEMORY.md
CAVEMAN_PROVIDER=claude python3 -m scripts /path/to/CLAUDE.md
```

Use any other model CLI:

```bash
CAVEMAN_LLM_COMMAND='my-llm --prompt-file {prompt_file}' python3 -m scripts /path/to/MEMORY.md
```

Large markdown files are compressed in heading-bounded chunks by default. This
keeps each model call small and validates each chunk before writing the final
file.

```bash
CAVEMAN_CHUNK_CHARS=8000 python3 -m scripts /path/to/MEMORY.md
CAVEMAN_CHUNKED=false python3 -m scripts /path/to/small-note.md
```

### What files work

| Type | Compress? |
|------|-----------|
| `.md`, `.txt`, `.rst`, `.typ`, `.typst`, `.tex` | ✅ Yes |
| Extensionless natural language | ✅ Yes |
| `.py`, `.js`, `.ts`, `.json`, `.yaml` | ❌ Skip (code/config) |
| `*.original.md` | ❌ Skip (backup files) |

## How It Work

```
/caveman-compress MEMORY.md
        ↓
detect file type        (no tokens)
        ↓
split large markdown into chunks
        ↓
model compresses chunks (tokens)
        ↓
validate chunks + final output (no tokens)
  checks: headings, code blocks, URLs, file paths, bullets
        ↓
if errors: model fixes cherry-picked issues only    (tokens — targeted fix)
  does NOT recompress — only patches broken parts
        ↓
retry up to 2 times
        ↓
write compressed → MEMORY.md
write original   → MEMORY.original.md
```

Only two things use tokens: initial compression + targeted fix if validation fails. Everything else is local Python.

## What Is Preserved

Caveman compress natural language. It never touch:

- Code blocks (` ``` ` fenced or indented)
- Inline code (`` `backtick content` ``)
- URLs and links
- File paths (`/src/components/...`)
- Commands (`npm install`, `git commit`)
- Technical terms, library names, API names
- Headings (exact text preserved)
- Tables (structure preserved, cell text compressed)
- Dates, version numbers, numeric values

## Why This Matter

Memory files load on **every session start**. A 1000-token project memory file costs tokens every single time you open a project. Over 100 sessions that's 100,000 tokens of overhead — just for context you already wrote.

Caveman cut that by ~46% on average. Same instructions. Same accuracy. Less waste.

```
┌────────────────────────────────────────────┐
│  TOKEN SAVINGS PER FILE    █████       46% │
│  SESSIONS THAT BENEFIT     ██████████ 100% │
│  INFORMATION PRESERVED     ██████████ 100% │
│  SETUP TIME                █            1x │
└────────────────────────────────────────────┘
```

## Part of Caveman

This skill is adapted from the [caveman](https://github.com/JuliusBrussee/caveman) toolkit — making coding agents use fewer tokens without losing accuracy.

- **caveman** — make agent *speak* like caveman (cuts response tokens ~65%)
- **caveman-compress** — make agent *read* less (cuts context tokens ~46%)
