#!/usr/bin/env python3
"""
Caveman Memory Compression Orchestrator

Usage:
    python scripts/compress.py <filepath>
"""

import os
import re
import shlex
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List

OUTER_FENCE_REGEX = re.compile(
    r"\A\s*(`{3,}|~{3,})[^\n]*\n(.*)\n\1\s*\Z", re.DOTALL
)

# Filenames and paths that almost certainly hold secrets or PII. Compressing
# them ships raw bytes to a model provider boundary that developers on sensitive
# codebases cannot cross. detect.py already skips .env by extension, but
# credentials.md / secrets.txt / ~/.aws/credentials would slip through the
# natural-language filter. This is a hard refuse before read.
SENSITIVE_BASENAME_REGEX = re.compile(
    r"(?ix)^("
    r"\.env(\..+)?"
    r"|\.netrc"
    r"|credentials(\..+)?"
    r"|secrets?(\..+)?"
    r"|passwords?(\..+)?"
    r"|id_(rsa|dsa|ecdsa|ed25519)(\.pub)?"
    r"|authorized_keys"
    r"|known_hosts"
    r"|.*\.(pem|key|p12|pfx|crt|cer|jks|keystore|asc|gpg)"
    r")$"
)

SENSITIVE_PATH_COMPONENTS = frozenset({".ssh", ".aws", ".gnupg", ".kube", ".docker"})

SENSITIVE_NAME_TOKENS = (
    "secret", "credential", "password", "passwd",
    "apikey", "accesskey", "token", "privatekey",
)


def is_sensitive_path(filepath: Path) -> bool:
    """Heuristic denylist for files that must never be shipped to a third-party API."""
    name = filepath.name
    if SENSITIVE_BASENAME_REGEX.match(name):
        return True
    lowered_parts = {p.lower() for p in filepath.parts}
    if lowered_parts & SENSITIVE_PATH_COMPONENTS:
        return True
    # Normalize separators so "api-key" and "api_key" both match "apikey".
    lower = re.sub(r"[_\-\s.]", "", name.lower())
    return any(tok in lower for tok in SENSITIVE_NAME_TOKENS)


def strip_llm_wrapper(text: str) -> str:
    """Strip outer ```markdown ... ``` fence when it wraps the entire output."""
    m = OUTER_FENCE_REGEX.match(text)
    if m:
        return m.group(2)
    return text

from .detect import should_compress
from .validate import validate, validate_text

MAX_RETRIES = 2
DEFAULT_CHUNK_CHARS = 12_000
CHUNKED_FILE_CHARS = 30_000
HEADING_LINE_REGEX = re.compile(r"^#{1,6}\s+")


# ---------- Model Calls ----------


def run_command(command: List[str], prompt: str, *, stdin: bool = True) -> str:
    try:
        result = subprocess.run(
            command,
            input=prompt if stdin else None,
            text=True,
            capture_output=True,
            check=True,
        )
        return strip_llm_wrapper(result.stdout)
    except FileNotFoundError as e:
        raise RuntimeError(f"Model command not found: {command[0]}") from e
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.strip() if e.stderr else "(no stderr)"
        raise RuntimeError(
            f"Model command failed ({' '.join(command)}):\n{stderr}"
        ) from e


def call_custom_command(prompt: str) -> str:
    """Run a user-supplied model command.

    If the command contains {prompt_file}, the prompt is written to a temporary
    file and the placeholder is replaced with that path. If it contains
    {prompt}, the prompt is passed as an argv value. Otherwise the prompt is
    sent on stdin.
    """
    command_template = os.environ["CAVEMAN_LLM_COMMAND"]
    parts = shlex.split(command_template)
    if not parts:
        raise RuntimeError("CAVEMAN_LLM_COMMAND is empty")

    if any("{prompt_file}" in part for part in parts):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(prompt)
            prompt_path = f.name
        try:
            command = [part.replace("{prompt_file}", prompt_path) for part in parts]
            return run_command(command, prompt, stdin=False)
        finally:
            Path(prompt_path).unlink(missing_ok=True)

    if any("{prompt}" in part for part in parts):
        command = [part.replace("{prompt}", prompt) for part in parts]
        return run_command(command, prompt, stdin=False)

    return run_command(parts, prompt, stdin=True)


def call_anthropic(prompt: str) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")

    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError("anthropic package is not installed") from e

    client = anthropic.Anthropic(api_key=api_key)
    msg = client.messages.create(
        model=os.environ.get("CAVEMAN_MODEL", "claude-sonnet-4-5"),
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )
    return strip_llm_wrapper(msg.content[0].text)


def call_claude(prompt: str) -> str:
    return run_command(["claude", "--print"], prompt)


def call_codex(prompt: str) -> str:
    model = os.environ.get("CAVEMAN_MODEL")
    command = [
        "codex",
        "exec",
        "--ephemeral",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
    ]
    if model:
        command.extend(["--model", model])
    command.append("-")
    return run_command(command, prompt)


def call_opencode(prompt: str) -> str:
    model = os.environ.get("CAVEMAN_MODEL")
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(prompt)
        prompt_path = f.name
    try:
        command = ["opencode", "run", "--dir", str(Path.cwd()), "--file", prompt_path]
        if model:
            command.extend(["--model", model])
        command.append("Execute the attached prompt. Return only the requested output.")
        return run_command(command, prompt, stdin=False)
    finally:
        Path(prompt_path).unlink(missing_ok=True)


def available_provider() -> str:
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    for provider, binary in (
        ("codex", "codex"),
        ("opencode", "opencode"),
        ("claude", "claude"),
    ):
        if shutil.which(binary):
            return provider
    raise RuntimeError(
        "No model provider available. Set CAVEMAN_PROVIDER or "
        "CAVEMAN_LLM_COMMAND, or install/login to codex, opencode, or claude."
    )


def call_model(prompt: str) -> str:
    if os.environ.get("CAVEMAN_LLM_COMMAND"):
        return call_custom_command(prompt)

    provider = os.environ.get("CAVEMAN_PROVIDER", "auto").lower()
    if provider == "auto":
        provider = available_provider()

    providers = {
        "anthropic": call_anthropic,
        "codex": call_codex,
        "opencode": call_opencode,
        "claude": call_claude,
    }
    if provider not in providers:
        raise RuntimeError(
            "Unsupported CAVEMAN_PROVIDER. Use one of: auto, anthropic, "
            "codex, opencode, claude."
        )
    return providers[provider](prompt)


def build_compress_prompt(original: str) -> str:
    return f"""
Compress this markdown into caveman format.

STRICT RULES:
- Do NOT modify anything inside ``` code blocks
- Do NOT modify anything inside inline backticks
- Preserve ALL URLs exactly
- Preserve ALL headings exactly
- Preserve file paths and commands
- Return ONLY the compressed markdown body — do NOT wrap the entire output in a ```markdown fence or any other fence. Inner code blocks from the original stay as-is; do not add a new outer fence around the whole file.

Only compress natural language.

TEXT:
{original}
"""


def build_chunk_compress_prompt(original: str, index: int, total: int) -> str:
    return f"""
Compress this markdown chunk into caveman format.

This is chunk {index} of {total}. It will be joined with other chunks.

STRICT RULES:
- Do NOT modify anything inside ``` code blocks
- Do NOT modify anything inside inline backticks
- Preserve ALL URLs exactly
- Preserve ALL headings exactly
- Preserve file paths and commands
- Do NOT summarize, omit sections, or collapse headings
- Return ONLY the compressed markdown chunk — no explanation and no outer fence

Only compress natural language.

CHUNK:
{original}
"""


def build_fix_prompt(original: str, compressed: str, errors: List[str]) -> str:
    errors_str = "\n".join(f"- {e}" for e in errors)
    return f"""You are fixing a caveman-compressed markdown file. Specific validation errors were found.

CRITICAL RULES:
- DO NOT recompress or rephrase the file
- ONLY fix the listed errors — leave everything else exactly as-is
- The ORIGINAL is provided as reference only (to restore missing content)
- Preserve caveman style in all untouched sections

ERRORS TO FIX:
{errors_str}

HOW TO FIX:
- Missing URL: find it in ORIGINAL, restore it exactly where it belongs in COMPRESSED
- Code block mismatch: find the exact code block in ORIGINAL, restore it in COMPRESSED
- Heading mismatch: restore the exact heading text from ORIGINAL into COMPRESSED
- Do not touch any section not mentioned in the errors

ORIGINAL (reference only):
{original}

COMPRESSED (fix this):
{compressed}

Return ONLY the fixed compressed file. No explanation.
"""


def is_heading_line(line: str) -> bool:
    return bool(HEADING_LINE_REGEX.match(line))


def split_markdown_sections(text: str) -> List[str]:
    """Split markdown at heading lines, ignoring headings inside fenced blocks."""
    sections = []
    current = []
    in_fence = False
    fence_char = ""
    fence_len = 0

    for line in text.splitlines(keepends=True):
        fence_match = re.match(r"^(\s{0,3})(`{3,}|~{3,})(.*)$", line.rstrip("\n"))
        if fence_match:
            marker = fence_match.group(2)
            marker_char = marker[0]
            marker_len = len(marker)
            suffix = fence_match.group(3).strip()
            if not in_fence:
                in_fence = True
                fence_char = marker_char
                fence_len = marker_len
            elif marker_char == fence_char and marker_len >= fence_len and suffix == "":
                in_fence = False
                fence_char = ""
                fence_len = 0

        if not in_fence and is_heading_line(line) and current:
            sections.append("".join(current))
            current = [line]
        else:
            current.append(line)

    if current:
        sections.append("".join(current))
    return sections


def build_chunks(text: str, max_chars: int) -> List[str]:
    sections = split_markdown_sections(text)
    chunks = []
    current = []
    current_len = 0

    for section in sections:
        section_len = len(section)
        if current and current_len + section_len > max_chars:
            chunks.append("".join(current))
            current = [section]
            current_len = section_len
        else:
            current.append(section)
            current_len += section_len

    if current:
        chunks.append("".join(current))
    return chunks


def should_chunk(original_text: str) -> bool:
    if os.environ.get("CAVEMAN_CHUNKED", "").lower() in {"0", "false", "no"}:
        return False
    return len(original_text) >= int(os.environ.get("CAVEMAN_CHUNKED_FILE_CHARS", CHUNKED_FILE_CHARS))


def compress_chunk(original_chunk: str, index: int, total: int) -> str:
    compressed = call_model(build_chunk_compress_prompt(original_chunk, index, total))

    if compressed is None or not compressed.strip():
        raise RuntimeError(f"Chunk {index}/{total}: model provider returned an empty response")

    result = validate_text(original_chunk, compressed)
    for attempt in range(MAX_RETRIES):
        if result.is_valid:
            return compressed

        print(f"❌ Chunk {index}/{total} validation failed:")
        for err in result.errors:
            print(f"   - {err}")

        if attempt == MAX_RETRIES - 1:
            raise RuntimeError(f"Chunk {index}/{total}: validation failed after retries")

        print(f"Fixing chunk {index}/{total} with model provider...")
        compressed = call_model(build_fix_prompt(original_chunk, compressed, result.errors))
        result = validate_text(original_chunk, compressed)

    return compressed


def compress_chunked(original_text: str) -> str:
    max_chars = int(os.environ.get("CAVEMAN_CHUNK_CHARS", DEFAULT_CHUNK_CHARS))
    chunks = build_chunks(original_text, max_chars)
    if len(chunks) <= 1:
        return call_model(build_compress_prompt(original_text))

    print(f"Chunked mode: {len(chunks)} chunks, target <= {max_chars} chars each")
    compressed_chunks = []

    for index, chunk in enumerate(chunks, start=1):
        print(f"Compressing chunk {index}/{len(chunks)} ({len(chunk)} chars)...")
        compressed_chunks.append(compress_chunk(chunk, index, len(chunks)))

    compressed = "".join(compressed_chunks)
    if compressed.strip() == original_text.strip():
        raise RuntimeError("Chunked compression produced output identical to input")
    return compressed


# ---------- Core Logic ----------


def compress_file(filepath: Path) -> bool:
    # Resolve and validate path
    filepath = filepath.resolve()
    MAX_FILE_SIZE = 500_000  # 500KB
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    if filepath.stat().st_size > MAX_FILE_SIZE:
        raise ValueError(f"File too large to compress safely (max 500KB): {filepath}")

    # Refuse files that look like they contain secrets or PII. Compressing ships
    # the raw bytes to a model provider boundary, so we fail
    # loudly rather than silently exfiltrate credentials or keys. Override is
    # intentional: the user must rename the file if the heuristic is wrong.
    if is_sensitive_path(filepath):
        raise ValueError(
            f"Refusing to compress {filepath}: filename looks sensitive "
            "(credentials, keys, secrets, or known private paths). "
            "Compression sends file contents to the configured model provider. "
            "Rename the file if this is a false positive."
        )

    print(f"Processing: {filepath}")

    if not should_compress(filepath):
        print("Skipping (not natural language)")
        return False

    original_text = filepath.read_text(errors="ignore")
    backup_path = filepath.with_name(filepath.stem + ".original.md")

    if not original_text.strip():
        print("❌ Refusing to compress: file is empty or whitespace-only.")
        return False

    # Check if backup already exists to prevent accidental overwriting
    if backup_path.exists():
        print(f"⚠️ Backup file already exists: {backup_path}")
        print("The original backup may contain important content.")
        print("Aborting to prevent data loss. Please remove or rename the backup file if you want to proceed.")
        return False

    # Step 1: Compress
    print("Compressing with model provider...")
    chunked_mode = should_chunk(original_text)
    try:
        compressed = compress_chunked(original_text) if chunked_mode else call_model(build_compress_prompt(original_text))
    except RuntimeError as e:
        print(f"❌ Compression aborted: {e}")
        print("   Original file is untouched (no backup created).")
        return False

    if compressed is None or not compressed.strip():
        print("❌ Compression aborted: model provider returned an empty response.")
        print("   Original file is untouched (no backup created).")
        return False

    if compressed.strip() == original_text.strip():
        print("❌ Compression aborted: output is identical to input.")
        print("   Likely causes: model refused, returned the prompt verbatim, or the file is")
        print("   already in caveman form. Original file is untouched (no backup created).")
        return False

    # Save original as backup, then verify the backup readback before
    # touching the input file. If the filesystem dropped bytes (encoding,
    # antivirus, disk full), unlink the bad backup and abort instead of
    # leaving the user with a corrupt backup + compressed primary.
    backup_path.write_text(original_text)
    backup_readback = backup_path.read_text(errors="ignore")
    if backup_readback != original_text:
        print(f"❌ Backup write verification failed: {backup_path}")
        print("   In-memory original differs from on-disk backup. Aborting before touching the input file.")
        try:
            backup_path.unlink()
        except OSError:
            pass
        return False
    filepath.write_text(compressed)

    # Step 2: Validate + Retry
    for attempt in range(MAX_RETRIES):
        print(f"\nValidation attempt {attempt + 1}")

        result = validate(backup_path, filepath)

        if result.is_valid:
            print("Validation passed")
            break

        print("❌ Validation failed:")
        for err in result.errors:
            print(f"   - {err}")

        if chunked_mode:
            filepath.write_text(original_text)
            backup_path.unlink(missing_ok=True)
            print("❌ Chunked output failed final validation — original restored")
            return False

        if attempt == MAX_RETRIES - 1:
            # Restore original on failure
            filepath.write_text(original_text)
            backup_path.unlink(missing_ok=True)
            print("❌ Failed after retries — original restored")
            return False

        print("Fixing with model provider...")
        compressed = call_model(
            build_fix_prompt(original_text, compressed, result.errors)
        )
        filepath.write_text(compressed)

    return True
