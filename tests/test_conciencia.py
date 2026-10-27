# Portions Copyright (c) 2026 Enrique Rocha (@soyenriquerocha) - see LICENSE for original authors
# SPDX-License-Identifier: MIT
# id: er-fd4fa55b
"""Campaign awareness ("conciencia de campaña") tests.

* ``ads/references/conciencia-schema.json`` must parse and declare its keys.
* ``scripts/conciencia.py`` must round-trip register / checkin / show / due /
  render against a temp HOME, keep unreported values as null (never 0), and
  only compute a ratio from check-ins where both sides were reported.
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
SCRIPT = REPO_ROOT / "scripts" / "conciencia.py"
KEY = "meta-120210000000001"


def _run(args: list[str], env: dict, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd,
        timeout=15,
    )


@pytest.fixture
def fake_home(tmp_path: Path) -> dict:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    return env


def _register(env: dict, **extra: str) -> subprocess.CompletedProcess:
    args = [
        "register", "--platform", "meta", "--campaign-id", "120210000000001",
        "--name", "WhatsApp Odontología", "--objective", "messages", "--channel", "whatsapp",
    ]
    for k, v in extra.items():
        args += [f"--{k.replace('_', '-')}", v]
    return _run(args, env)


def _checkin(env: dict, payload: dict) -> subprocess.CompletedProcess:
    return _run(["checkin", KEY, "--json", json.dumps(payload)], env)


def _record_path(env: dict) -> Path:
    return Path(env["HOME"]) / ".claude-ads" / "conciencia" / f"{KEY}.json"


# --------------------------------------------------------------------------- #
# Schema                                                                      #
# --------------------------------------------------------------------------- #

def test_schema_parses_and_declares_required_keys() -> None:
    data = json.loads((REFERENCES_DIR / "conciencia-schema.json").read_text("utf-8"))
    for key in ("campaign", "knowns", "unknowns", "checkins", "next_checkin_at", "status"):
        assert key in data["required"]
    checkin = data["definitions"]["checkin"]["properties"]
    assert set(checkin["user_reported"]["properties"]) >= {"conversations", "qualified", "closed", "revenue", "junk"}


def test_record_keys_match_schema(fake_home: dict) -> None:
    _register(fake_home)
    rec = json.loads(_record_path(fake_home).read_text("utf-8"))
    schema = json.loads((REFERENCES_DIR / "conciencia-schema.json").read_text("utf-8"))
    assert set(rec) == set(schema["properties"])
    assert set(rec["campaign"]) == set(schema["properties"]["campaign"]["properties"])


# --------------------------------------------------------------------------- #
# Round-trip                                                                  #
# --------------------------------------------------------------------------- #

def test_register_is_idempotent(fake_home: dict) -> None:
    p1 = _register(fake_home)
    assert p1.returncode == 0, p1.stderr
    assert json.loads(p1.stdout)["created"] is True
    p2 = _register(fake_home)
    assert json.loads(p2.stdout)["created"] is False


def test_show_missing_campaign_exits_2(fake_home: dict) -> None:
    assert _run(["show", KEY], fake_home).returncode == 2


def test_checkin_derives_close_rate_and_cost_per_close(fake_home: dict) -> None:
    _register(fake_home, ticket_value="200")
    p = _checkin(fake_home, {
        "period_from": "2026-10-01", "period_to": "2026-10-07",
        "source_of_platform_metrics": "mcp",
        "platform_metrics": {"spend": 300, "clicks": 800, "messages": 50},
        "user_reported": {"conversations": 40, "qualified": 12, "closed": 6, "junk": 20},
    })
    assert p.returncode == 0, p.stderr

    out = json.loads(_run(["show", KEY], fake_home).stdout)
    cum = out["metrics"]["cumulative"]
    assert cum["close_rate"] == {"value": 0.15, "checkins": 1}
    assert cum["cost_per_close"]["value"] == 50.0
    assert cum["junk_rate"]["value"] == 0.5
    assert cum["platform_vs_real"]["value"] == 0.8
    assert cum["estimated_roas"]["value"] == 4.0
    assert cum["real_roas"]["value"] is None  # revenue never reported


def test_unreported_fields_stay_null_and_listed_as_unknown(fake_home: dict) -> None:
    _register(fake_home)
    _checkin(fake_home, {"user_reported": {"conversations": 10}})
    rec = json.loads(_record_path(fake_home).read_text("utf-8"))
    ur = rec["checkins"][0]["user_reported"]
    assert ur["closed"] is None and ur["junk"] is None
    assert ur["conversations"] == 10
    assert any("cerrados" in u for u in rec["unknowns"])
    assert not any(u.startswith("Conversaciones reales") for u in rec["unknowns"])

    cum = json.loads(_run(["show", KEY], fake_home).stdout)["metrics"]["cumulative"]
    assert cum["close_rate"]["value"] is None
    assert cum["totals"]["closed"] is None


def test_ratio_only_uses_checkins_with_both_sides(fake_home: dict) -> None:
    _register(fake_home)
    _checkin(fake_home, {"user_reported": {"conversations": 20, "closed": 2}})
    _checkin(fake_home, {"user_reported": {"conversations": 30}})  # closed unknown
    out = json.loads(_run(["show", KEY], fake_home).stdout)
    assert out["metrics"]["cumulative"]["close_rate"] == {"value": 0.1, "checkins": 1}
    assert out["metrics"]["trend"]["close_rate"] is None


def test_checkin_rejects_bad_values(fake_home: dict) -> None:
    _register(fake_home)
    assert _checkin(fake_home, {"user_reported": {"closed": -1}}).returncode == 3
    assert _checkin(fake_home, {"user_reported": {"closed": 2.5}}).returncode == 3
    assert _checkin(fake_home, {"user_reported": {"sold": 2}}).returncode == 3


# --------------------------------------------------------------------------- #
# Due / render                                                                #
# --------------------------------------------------------------------------- #

def test_due_lists_only_overdue_campaigns(fake_home: dict) -> None:
    _register(fake_home)
    assert json.loads(_run(["due"], fake_home).stdout)["due"] == []

    path = _record_path(fake_home)
    rec = json.loads(path.read_text("utf-8"))
    rec["next_checkin_at"] = "2020-01-01T00:00:00Z"
    path.write_text(json.dumps(rec), encoding="utf-8")
    due = json.loads(_run(["due"], fake_home).stdout)["due"]
    assert [d["key"] for d in due] == [KEY]

    _run(["snooze", KEY, "--days", "1"], fake_home)
    assert json.loads(_run(["due"], fake_home).stdout)["due"] == []


def test_pixel_campaigns_are_never_due(fake_home: dict) -> None:
    _run([
        "register", "--platform", "meta", "--campaign-id", "shop1", "--name", "Tienda",
        "--objective", "sales", "--channel", "pixel_purchase", "--every", "1",
    ], fake_home)
    path = Path(fake_home["HOME"]) / ".claude-ads" / "conciencia" / "meta-shop1.json"
    rec = json.loads(path.read_text("utf-8"))
    assert rec["campaign"]["tracking_mode"] == "pixel"
    rec["next_checkin_at"] = "2020-01-01T00:00:00Z"
    path.write_text(json.dumps(rec), encoding="utf-8")
    assert json.loads(_run(["due"], fake_home).stdout)["due"] == []


def test_render_writes_known_and_unknown_sections(fake_home: dict, tmp_path: Path) -> None:
    _register(fake_home)
    _checkin(fake_home, {
        "platform_metrics": {"spend": 300},
        "user_reported": {"conversations": 40, "closed": 6, "notes": "2 pidieron cotización"},
    })
    out = tmp_path / "conciencia-de-campana.md"
    p = _run(["render", KEY, "--out", str(out)], fake_home)
    assert p.returncode == 0, p.stderr
    md = out.read_text("utf-8")
    assert "## Lo que sé" in md and "## Lo que no sé" in md
    assert "15.0 %" in md
    assert "N/A" in md
    assert "2 pidieron cotización" in md
