"""Agent definition tests.

Every ``agents/*.md`` must:

* Have a parseable YAML frontmatter block.
* Declare ``name``, ``description``, ``model``, and ``tools``.
* Use a known Claude model family.
* Only reference reference files / agents that actually exist.

These checks catch agent drift before it shows up at audit time.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from tests._helpers import (
    REPO_ROOT,
    find_agent_links,
    find_reference_links,
    read_frontmatter,
)

AGENT_FILES = sorted((REPO_ROOT / "agents").glob("*.md"))

# Accept friendly names (opus/sonnet/haiku) OR specific model IDs.
ALLOWED_MODELS = {"opus", "sonnet", "haiku"}


@pytest.mark.parametrize("agent_path", AGENT_FILES, ids=lambda p: p.stem)
def test_agent_frontmatter(agent_path: Path) -> None:
    fm, _ = read_frontmatter(agent_path)
    assert fm, f"{agent_path}: frontmatter missing or unparseable"
    for key in ("name", "description", "model", "tools"):
        assert key in fm, f"{agent_path}: frontmatter missing `{key}`"


@pytest.mark.parametrize("agent_path", AGENT_FILES, ids=lambda p: p.stem)
def test_agent_name_matches_filename(agent_path: Path) -> None:
    fm, _ = read_frontmatter(agent_path)
    expected = agent_path.stem
    assert fm.get("name") == expected, (
        f"{agent_path}: name={fm.get('name')!r} must match filename {expected!r}"
    )


@pytest.mark.parametrize("agent_path", AGENT_FILES, ids=lambda p: p.stem)
def test_agent_model_recognised(agent_path: Path) -> None:
    fm, _ = read_frontmatter(agent_path)
    model = fm.get("model", "").strip().lower()
    # Allow either a family alias or a full model ID containing the family name.
    assert any(family in model for family in ALLOWED_MODELS), (
        f"{agent_path}: unknown model {model!r}; expected one of {ALLOWED_MODELS}"
    )


@pytest.mark.parametrize("agent_path", AGENT_FILES, ids=lambda p: p.stem)
def test_agent_references_exist(agent_path: Path) -> None:
    _, body = read_frontmatter(agent_path)
    missing: list[str] = []
    for ref in find_reference_links(body):
        if not (REPO_ROOT / ref).exists():
            missing.append(ref)
    for agent in find_agent_links(body):
        if not (REPO_ROOT / "agents" / f"{agent}.md").exists():
            missing.append(f"agents/{agent}.md")
    assert not missing, f"{agent_path}: broken references → {missing}"
