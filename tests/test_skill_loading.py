"""Skill-loading tests.

Every SKILL.md under skills/ and the top-level ads/SKILL.md must:

* Have a parseable YAML frontmatter block.
* Declare a ``name`` and ``description``.
* Match the parent directory name (for sub-skills).
* Only reference files that actually exist (ads/references/*, scripts/*, agents/*).

These checks are the safety net for adding new platforms or integrations
without silently breaking the orchestrator.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from tests._helpers import (
    REPO_ROOT,
    find_agent_links,
    find_reference_links,
    find_script_links,
    read_frontmatter,
)

SKILL_FILES = sorted(
    [REPO_ROOT / "ads" / "SKILL.md"]
    + list((REPO_ROOT / "skills").glob("*/SKILL.md"))
)


@pytest.mark.parametrize("skill_path", SKILL_FILES, ids=lambda p: p.parent.name)
def test_frontmatter_parses(skill_path: Path) -> None:
    fm, _ = read_frontmatter(skill_path)
    assert fm, f"{skill_path}: frontmatter missing or unparseable"
    assert "name" in fm, f"{skill_path}: frontmatter missing `name`"
    assert "description" in fm, f"{skill_path}: frontmatter missing `description`"


@pytest.mark.parametrize("skill_path", SKILL_FILES, ids=lambda p: p.parent.name)
def test_name_matches_directory(skill_path: Path) -> None:
    fm, _ = read_frontmatter(skill_path)
    parent_name = skill_path.parent.name
    if parent_name == "ads":
        # Top-level orchestrator; convention is name == "ads".
        assert fm.get("name") == "ads", f"{skill_path}: expected name 'ads'"
    else:
        assert fm.get("name") == parent_name, (
            f"{skill_path}: name={fm.get('name')!r} does not match directory {parent_name!r}"
        )


@pytest.mark.parametrize("skill_path", SKILL_FILES, ids=lambda p: p.parent.name)
def test_referenced_files_exist(skill_path: Path) -> None:
    _, body = read_frontmatter(skill_path)
    missing: list[str] = []

    for ref in find_reference_links(body):
        if not (REPO_ROOT / ref).exists():
            missing.append(ref)

    for script in find_script_links(body):
        # Scripts can be referenced as scripts/foo.py (relative to repo root)
        # or scripts/foo.py (relative to skill dir). Accept either.
        if not (REPO_ROOT / script).exists() and not (REPO_ROOT / "ads" / script).exists():
            missing.append(script)

    for agent in find_agent_links(body):
        if not (REPO_ROOT / "agents" / f"{agent}.md").exists():
            missing.append(f"agents/{agent}.md")

    assert not missing, f"{skill_path}: broken references → {missing}"
