#!/usr/bin/env python3
"""
Agent Config Sync — align all coding agents to a chosen baseline.

Usage:
    python sync.py                           # dry-run from codex baseline
    python sync.py --baseline kimi           # dry-run from kimi baseline
    python sync.py --yes                     # apply from codex baseline
    python sync.py --baseline opencode --yes # apply from opencode baseline
"""

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

# ── Configuration ───────────────────────────────────────────────────────────

AGENTS = {
    "codex": {
        "agents": Path.home() / ".codex" / "AGENTS.md",
        "skills": Path.home() / ".codex" / "skills",
        "path_prefix": "/Users/roman/.codex",
    },
    "opencode": {
        "agents": Path.home() / ".config" / "opencode" / "AGENTS.md",
        "skills": Path.home() / ".opencode" / "skills",
        "path_prefix": "/Users/roman/.config/opencode",
    },
    "kimi": {
        "agents": Path.home() / ".kimi" / "AGENTS.md",
        "skills": Path.home() / ".kimi" / "skills",
        "path_prefix": "/Users/roman/.kimi",
    },
}

IGNORED_NAMES = {".system", ".DS_Store", ".tmp", ".git", "__pycache__", ".venv", ".env"}

# ── Helpers ─────────────────────────────────────────────────────────────────


def dir_tree_same(left: Path, right: Path) -> bool:
    """Deep comparison: True only if both trees have identical files and contents."""
    if not right.exists():
        return False
    cmp = filecmp.dircmp(str(left), str(right), ignore=list(IGNORED_NAMES))
    # Any file unique to either side, or any differing file → not same
    if cmp.left_only or cmp.right_only or cmp.diff_files:
        return False
    # Recurse into common subdirectories
    for sub in cmp.common_dirs:
        if not dir_tree_same(left / sub, right / sub):
            return False
    return True


def copy_tree(src: Path, dst: Path) -> None:
    """Copy a directory tree, overwriting destination, ignoring junk files."""
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns(*IGNORED_NAMES),
    )


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


# ── Core logic ──────────────────────────────────────────────────────────────


def adapt_agents_md(content: str, baseline: str, target: str) -> str:
    """Replace baseline-specific paths with target-agent equivalents."""
    baseline_prefix = AGENTS[baseline]["path_prefix"]
    target_prefix = AGENTS[target]["path_prefix"]
    return content.replace(baseline_prefix, target_prefix)


def sync_agents(baseline: str, target: str, dry_run: bool) -> list[str]:
    """Sync AGENTS.md from baseline to target. Returns log lines."""
    logs: list[str] = []
    src_path = AGENTS[baseline]["agents"]
    tgt_path = AGENTS[target]["agents"]
    ensure_dir(tgt_path.parent)

    if not src_path.exists():
        logs.append(f"  ⚠️  Baseline AGENTS.md missing; skipping {target}.")
        return logs

    source_text = src_path.read_text(encoding="utf-8")
    adapted_text = adapt_agents_md(source_text, baseline, target)

    needs_write = True
    if tgt_path.exists():
        try:
            target_text = tgt_path.read_text(encoding="utf-8")
            needs_write = target_text != adapted_text
        except OSError:
            needs_write = True

    if needs_write:
        action = "would update" if dry_run else "updated"
        logs.append(f"  📄 AGENTS.md → {action} ({target})")
        if not dry_run:
            tgt_path.write_text(adapted_text, encoding="utf-8")
    else:
        logs.append(f"  ✅ AGENTS.md already aligned ({target})")

    return logs


def sync_skills(baseline: str, target: str, dry_run: bool) -> list[str]:
    """Sync skills from baseline to target. Returns log lines."""
    logs: list[str] = []
    src_skills = AGENTS[baseline]["skills"]
    tgt_skills = AGENTS[target]["skills"]
    ensure_dir(tgt_skills)

    if not src_skills.exists():
        logs.append(f"  ⚠️  Baseline skills dir missing; skipping {target}.")
        return logs

    source_skills = [
        d for d in src_skills.iterdir()
        if d.is_dir() and d.name not in IGNORED_NAMES
    ]

    for skill in sorted(source_skills, key=lambda p: p.name):
        dst = tgt_skills / skill.name
        if dst.exists() and dir_tree_same(skill, dst):
            logs.append(f"  ✅ {skill.name} already aligned ({target})")
        else:
            action = "would overwrite" if dst.exists() else "would copy"
            if not dry_run:
                copy_tree(skill, dst)
                action = "overwritten" if dst.exists() else "copied"
            logs.append(f"  📦 {skill.name} → {action} ({target})")

    return logs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync agent config (AGENTS.md + skills) from a baseline to all other agents."
    )
    parser.add_argument(
        "--baseline",
        default="codex",
        choices=list(AGENTS.keys()),
        help="Agent to use as source of truth (default: codex).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=None,
        help="Show what would change without applying.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Apply changes.",
    )
    args = parser.parse_args()

    # Default to dry-run unless --yes is explicitly passed.
    dry_run = True if args.dry_run is None and not args.yes else bool(args.dry_run)
    baseline = args.baseline

    # Validate baseline exists
    if not AGENTS[baseline]["agents"].exists():
        print(f"Error: Baseline AGENTS.md not found for '{baseline}'.", file=sys.stderr)
        return 1
    if not AGENTS[baseline]["skills"].exists():
        print(f"Error: Baseline skills dir not found for '{baseline}'.", file=sys.stderr)
        return 1

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== Agent Config Sync [{mode}] | Baseline: {baseline.upper()} ===\n")

    any_changes = False

    for target_name in AGENTS:
        if target_name == baseline:
            continue
        print(f"▶ {target_name.upper()}")
        logs = []
        logs.extend(sync_agents(baseline, target_name, dry_run))
        logs.extend(sync_skills(baseline, target_name, dry_run))
        for line in logs:
            print(line)
            if "→" in line:
                any_changes = True
        print()

    if dry_run:
        if any_changes:
            print("Run with --yes to apply the above changes.")
        else:
            print("Everything is already aligned. No changes needed.")
    else:
        if any_changes:
            print("Sync complete.")
        else:
            print("Everything was already aligned.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
