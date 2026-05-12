"""Reference-file integrity tests.

* Every ``ads/references/*.md`` must be ≤200 lines (project rule from
  ``CLAUDE.md``).
* ``audit-output-schema.json`` must be valid JSON-Schema-shaped.

If a reference legitimately needs more than 200 lines, the right move is to
split it into focused sub-files and turn the original into an index, not to
suppress the check.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests._helpers import REPO_ROOT

REFERENCES_DIR = REPO_ROOT / "ads" / "references"

REFERENCE_FILES = sorted(REFERENCES_DIR.glob("*.md"))
MAX_LINES = 200


@pytest.mark.parametrize("ref_path", REFERENCE_FILES, ids=lambda p: p.name)
def test_reference_under_line_budget(ref_path: Path) -> None:
    line_count = sum(1 for _ in ref_path.open("r", encoding="utf-8"))
    assert line_count <= MAX_LINES, (
        f"{ref_path.name}: {line_count} lines > {MAX_LINES} limit. "
        f"Split into focused sub-files and convert the original into an index."
    )


def test_audit_output_schema_is_valid_json() -> None:
    schema_path = REFERENCES_DIR / "audit-output-schema.json"
    assert schema_path.exists(), "audit-output-schema.json is missing"
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    # Sanity-check the schema shape: top-level type, required fields documented.
    assert data.get("type") == "object", "schema root must be type=object"
    assert "platform" in data.get("properties", {}), "schema missing 'platform' property"
    assert "checks" in data.get("properties", {}), "schema missing 'checks' property"
    assert "health_score" in data.get("required", []), (
        "schema must require 'health_score'"
    )
