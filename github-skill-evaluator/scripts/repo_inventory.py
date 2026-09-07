#!/usr/bin/env python3
"""Inventory a local skill repository without judging its quality.

Stdlib-only. Emits JSON with likely evaluation-relevant files and simple counts.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

IGNORE_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__", ".next"}
INTERESTING_NAMES = {
    "SKILL.md", "README.md", "LICENSE", "LICENSE.md", "LICENSE.txt",
    "pyproject.toml", "package.json", "requirements.txt", "Cargo.toml",
    "Makefile", "Dockerfile", ".mcp.json",
}
INTERESTING_DIRS = {"scripts", "references", "examples", "tests", "test", "evals", "fixtures", "agents", "hooks", ".github"}


def inventory(root: Path) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")

    files: list[str] = []
    skill_files: list[str] = []
    relevant: list[str] = []
    ext_counts: dict[str, int] = {}

    for current, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        current_path = Path(current)
        rel_dir = current_path.relative_to(root)
        for name in names:
            p = current_path / name
            rel = str(p.relative_to(root))
            files.append(rel)
            suffix = p.suffix.lower() or "<none>"
            ext_counts[suffix] = ext_counts.get(suffix, 0) + 1
            if name == "SKILL.md":
                skill_files.append(rel)
            if (
                name in INTERESTING_NAMES
                or any(part in INTERESTING_DIRS for part in rel_dir.parts)
                or name.endswith((".yml", ".yaml", ".json", ".toml", ".sh", ".py", ".js", ".ts", ".md"))
            ):
                relevant.append(rel)

    return {
        "root": str(root),
        "file_count": len(files),
        "skill_files": sorted(skill_files),
        "relevant_files": sorted(relevant),
        "extension_counts": dict(sorted(ext_counts.items())),
        "notes": [
            "This is a navigation inventory, not a quality score.",
            "Inspect material files before scoring; do not infer sophistication from counts.",
        ],
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} /path/to/repo", file=sys.stderr)
        return 2
    try:
        result = inventory(Path(sys.argv[1]))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
