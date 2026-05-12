"""Shared test helpers — no external dependencies.

Keeping these in one place avoids re-implementing the frontmatter parser
across each test file. The YAML used in this repo's frontmatter is simple
(flat key: value pairs, occasional multi-line via ``>`` folded scalars), so
we parse it with a small hand-rolled function rather than pulling PyYAML
into requirements.txt.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def find_repo_root() -> Path:
    """Return the repo root regardless of cwd."""
    return REPO_ROOT


def read_frontmatter(md_path: Path) -> tuple[dict[str, str], str]:
    """Parse YAML-ish frontmatter from a Markdown file.

    Returns ``(frontmatter_dict, body)``. If no frontmatter is present
    returns ``({}, full_text)``.
    """
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text

    # Locate the closing '---' line.
    end_match = re.search(r"^---\s*$", text[4:], re.MULTILINE)
    if not end_match:
        return {}, text

    fm_block = text[4 : 4 + end_match.start()]
    body = text[4 + end_match.end() :].lstrip("\n")

    fm: dict[str, str] = {}
    current_key: str | None = None
    folded_lines: list[str] = []
    folded_active = False

    for raw_line in fm_block.splitlines():
        line = raw_line.rstrip()

        # Continuation of a folded scalar (>) — indented line.
        if folded_active and (line.startswith("  ") or line == ""):
            folded_lines.append(line.strip())
            continue
        if folded_active:
            # Folded scalar ended; flush.
            fm[current_key] = " ".join(s for s in folded_lines if s)
            folded_active = False
            folded_lines = []

        m = re.match(r"^([A-Za-z][A-Za-z0-9_\-]*):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        current_key = key
        if value == ">":
            folded_active = True
            folded_lines = []
            continue
        # Strip wrapping quotes if present.
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        fm[key] = value

    if folded_active and current_key is not None:
        fm[current_key] = " ".join(s for s in folded_lines if s)

    return fm, body


def find_reference_links(body: str) -> set[str]:
    """Return the set of ``ads/references/*.{md,json}`` paths referenced in body text."""
    pattern = re.compile(r"ads/references/[A-Za-z0-9_\-/]+\.(?:md|json)")
    return set(pattern.findall(body))


def find_script_links(body: str) -> set[str]:
    """Return the set of ``scripts/*.py`` paths referenced in body text."""
    pattern = re.compile(r"scripts/[A-Za-z0-9_\-/]+\.py")
    return set(pattern.findall(body))


def find_agent_links(body: str) -> set[str]:
    """Return agent names referenced in body text.

    Matches only the exact set of agents that exist in ``agents/``. The
    lookbehind/lookahead prevents false positives like ``meta-audit-results``
    being parsed as a reference to a nonexistent ``audit-results`` agent.
    """
    # Lookbehind: not preceded by a letter or a hyphen (so "meta-audit-..." doesn't match).
    # Lookahead: not followed by a letter or hyphen (so "audit-results" doesn't match a sub-string).
    pattern = re.compile(
        r"(?<![A-Za-z\-])"
        r"(audit-google|audit-meta|audit-tiktok"
        r"|creative-strategist|visual-designer|copy-writer|format-adapter)"
        r"(?![A-Za-z\-])"
    )
    return set(pattern.findall(body))
