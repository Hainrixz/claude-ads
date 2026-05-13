"""Profile + audit-history schema tests.

* ``ads/references/profile-schema.json`` and
  ``ads/references/audit-history-schema.json`` must be valid JSON-Schema-
  shaped.
* ``scripts/profile.py`` must round-trip through init / set / get / save-audit
  / compare / reset against an isolated temporary HOME — proving the schema
  contract and the utility stay in sync.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tests._helpers import REPO_ROOT

REFERENCES_DIR = REPO_ROOT / "ads" / "references"
PROFILE_SCRIPT = REPO_ROOT / "scripts" / "profile.py"


# --------------------------------------------------------------------------- #
# 1. Schema files are well-formed                                             #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "schema_name",
    ["profile-schema.json", "audit-history-schema.json"],
)
def test_schema_is_valid_json_schema(schema_name: str) -> None:
    schema_path = REFERENCES_DIR / schema_name
    assert schema_path.exists(), f"{schema_name} missing from references/"
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    assert data.get("type") == "object", (
        f"{schema_name}: schema root must be type=object"
    )
    assert "properties" in data, f"{schema_name}: missing 'properties'"
    assert "$schema" in data, f"{schema_name}: missing '$schema' declaration"


def test_profile_schema_has_required_top_keys() -> None:
    data = json.loads((REFERENCES_DIR / "profile-schema.json").read_text("utf-8"))
    required = set(data.get("required", []))
    for key in ("version", "context", "connections", "preferences", "zernio"):
        assert key in required, f"profile-schema.json: '{key}' not in required"


def test_profile_schema_platform_definition_shape() -> None:
    data = json.loads((REFERENCES_DIR / "profile-schema.json").read_text("utf-8"))
    pc = data.get("definitions", {}).get("platformConnection", {})
    props = pc.get("properties", {})
    for key in ("tier", "ad_account_id", "connected_at", "last_verified_at"):
        assert key in props, f"platformConnection missing '{key}'"


# --------------------------------------------------------------------------- #
# 2. scripts/profile.py round-trip                                            #
# --------------------------------------------------------------------------- #

def _run(args: list[str], env: dict) -> subprocess.CompletedProcess:
    """Invoke profile.py with a clean env scoped to a temp HOME."""
    return subprocess.run(
        [sys.executable, str(PROFILE_SCRIPT), *args],
        capture_output=True,
        text=True,
        env=env,
        timeout=15,
    )


@pytest.fixture
def fake_home(tmp_path: Path) -> dict:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    return env


def test_profile_help_exits_clean() -> None:
    proc = subprocess.run(
        [sys.executable, str(PROFILE_SCRIPT), "--help"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert proc.returncode == 0, proc.stderr
    assert "init" in proc.stdout and "save-audit" in proc.stdout


def test_get_returns_exit_2_when_profile_missing(fake_home: dict) -> None:
    proc = _run(["get"], fake_home)
    assert proc.returncode == 2, (
        f"expected exit 2 on missing profile, got {proc.returncode}\n"
        f"stdout: {proc.stdout}\nstderr: {proc.stderr}"
    )


def test_init_creates_profile_and_is_idempotent(fake_home: dict) -> None:
    p1 = _run(["init"], fake_home)
    assert p1.returncode == 0
    assert json.loads(p1.stdout)["created"] is True

    p2 = _run(["init"], fake_home)
    assert p2.returncode == 0
    assert json.loads(p2.stdout)["created"] is False


def test_set_then_get_roundtrip(fake_home: dict) -> None:
    _run(["init"], fake_home)
    _run(["set", "context.industry", "ecommerce"], fake_home)
    _run(["set", "context.monthly_spend_usd", "5000"], fake_home)
    _run(["set", "context.active_platforms", '["meta","tiktok"]'], fake_home)

    out = _run(["get", "--key", "context.industry"], fake_home)
    assert out.returncode == 0
    assert json.loads(out.stdout) == "ecommerce"

    out = _run(["get", "--key", "context.monthly_spend_usd"], fake_home)
    assert json.loads(out.stdout) == 5000

    out = _run(["get", "--key", "context.active_platforms"], fake_home)
    assert json.loads(out.stdout) == ["meta", "tiktok"]


def test_save_audit_appends_history_and_compare_diffs(fake_home: dict, tmp_path: Path) -> None:
    _run(["init"], fake_home)

    a1 = tmp_path / "meta-1.json"
    a1.write_text(json.dumps({
        "platform": "meta",
        "health_score": 60,
        "grade": "D",
        "critical_issues": [{"id": "M02"}, {"id": "M07"}],
    }))
    a2 = tmp_path / "meta-2.json"
    a2.write_text(json.dumps({
        "platform": "meta",
        "health_score": 75,
        "grade": "B",
        "critical_issues": [{"id": "M07"}],
        "checks": [{"id": "M11", "result": "FAIL"}],
    }))

    assert _run(["save-audit", str(a1)], fake_home).returncode == 0
    assert _run(["save-audit", str(a2)], fake_home).returncode == 0

    out = _run(["compare", "meta"], fake_home)
    assert out.returncode == 0
    diff = json.loads(out.stdout)
    assert diff["comparable"] is True
    assert diff["score_delta"] == 15
    assert "M02" in diff["resolved_issues"]
    assert "M11" in diff["new_issues"]


def test_compare_handles_insufficient_history(fake_home: dict) -> None:
    _run(["init"], fake_home)
    out = _run(["compare", "google"], fake_home)
    assert out.returncode == 0
    assert json.loads(out.stdout)["comparable"] is False


def test_reset_with_yes_wipes_dir(fake_home: dict, tmp_path: Path) -> None:
    _run(["init"], fake_home)
    assert (tmp_path / ".claude-ads" / "profile.json").exists()
    proc = _run(["reset", "--yes"], fake_home)
    assert proc.returncode == 0
    assert not (tmp_path / ".claude-ads").exists()


def test_profile_shape_matches_schema_keys(fake_home: dict) -> None:
    """The profile produced by init has every required top-level key the schema declares."""
    _run(["init"], fake_home)
    out = _run(["get"], fake_home)
    assert out.returncode == 0
    profile = json.loads(out.stdout)

    schema = json.loads((REFERENCES_DIR / "profile-schema.json").read_text("utf-8"))
    for key in schema.get("required", []):
        assert key in profile, f"init output missing required key '{key}'"
