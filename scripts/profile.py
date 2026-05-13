#!/usr/bin/env python3
"""claude-ads profile utility — pure-stdlib CLI for ~/.claude-ads/profile.json
and ~/.claude-ads/history/.

Subcommands
-----------
  init                        Create empty profile if missing. Idempotent.
  get [--key <dot.path>]      Print profile (or sub-key) as JSON.
  set <dot.path> <value>      Update a field (creates intermediate dicts).
  save-audit <results.json>   Copy audit JSON into history/, append index entry.
  compare <platform>          Diff most-recent vs previous audit for a platform.
  reset [--yes]               Wipe profile.json + history/ (asks unless --yes).

Exit codes
----------
  0  success
  2  profile not found (for `get` to signal "first run" to the orchestrator)
  3  validation / argument error
  4  IO error

All commands emit JSON on stdout (or empty on success when nothing to print) so
the agent can parse them. Errors print a single JSON line to stderr and exit
non-zero.

This script intentionally has zero non-stdlib imports.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any

# --------------------------------------------------------------------------- #
# Paths                                                                       #
# --------------------------------------------------------------------------- #

HOME = Path(os.environ.get("HOME") or os.path.expanduser("~"))
ROOT = HOME / ".claude-ads"
PROFILE = ROOT / "profile.json"
HISTORY = ROOT / "history"
INDEX = HISTORY / "index.json"

PROFILE_VERSION = "1.0"
HISTORY_VERSION = "1.0"


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #

def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _empty_profile() -> dict[str, Any]:
    now = _now()
    return {
        "version": PROFILE_VERSION,
        "created_at": now,
        "updated_at": now,
        "context": {
            "industry": None,
            "monthly_spend_usd": None,
            "primary_goal": None,
            "active_platforms": [],
        },
        "connections": {
            p: {
                "tier": None,
                "ad_account_id": None,
                "connected_at": None,
                "last_verified_at": None,
            }
            for p in ("meta", "google", "tiktok")
        },
        "zernio": {
            "signed_up": False,
            "api_key_present": False,
            "connected_socials": [],
        },
        "preferences": {
            "default_audit_depth": "default",
            "report_format": "md",
            "language": "en",
        },
        "last_command": None,
        "last_command_at": None,
    }


def _empty_index() -> dict[str, Any]:
    return {"version": HISTORY_VERSION, "audits": []}


def _die(msg: str, code: int = 3) -> None:
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(code)


def _load_json(p: Path, default: Any) -> Any:
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        _die(f"{p}: invalid JSON ({e})", 4)


def _write_json(p: Path, data: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    tmp.replace(p)


def _coerce(value: str) -> Any:
    """Best-effort JSON parse of a CLI argument. Strings stay strings."""
    s = value.strip()
    if not s:
        return ""
    if s.lower() in ("true", "false"):
        return s.lower() == "true"
    if s.lower() == "null":
        return None
    try:
        return json.loads(s)  # numbers, JSON arrays, JSON objects
    except json.JSONDecodeError:
        return s


def _dive(d: dict[str, Any], path: list[str]) -> Any:
    cur: Any = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    return cur


def _plant(d: dict[str, Any], path: list[str], value: Any) -> None:
    cur = d
    for k in path[:-1]:
        if k not in cur or not isinstance(cur[k], dict):
            cur[k] = {}
        cur = cur[k]
    cur[path[-1]] = value


# --------------------------------------------------------------------------- #
# Subcommands                                                                 #
# --------------------------------------------------------------------------- #

def cmd_init(args: argparse.Namespace) -> int:
    if PROFILE.exists():
        print(json.dumps({"created": False, "path": str(PROFILE)}))
        return 0
    _write_json(PROFILE, _empty_profile())
    HISTORY.mkdir(parents=True, exist_ok=True)
    if not INDEX.exists():
        _write_json(INDEX, _empty_index())
    print(json.dumps({"created": True, "path": str(PROFILE)}))
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    if not PROFILE.exists():
        # Exit 2 is the agent's signal for "no profile, offer /ads start".
        print(json.dumps({"missing": True, "path": str(PROFILE)}), file=sys.stderr)
        return 2
    data = _load_json(PROFILE, _empty_profile())
    if args.key:
        value = _dive(data, args.key.split("."))
        print(json.dumps(value))
    else:
        print(json.dumps(data, indent=2))
    return 0


def cmd_set(args: argparse.Namespace) -> int:
    if not PROFILE.exists():
        _write_json(PROFILE, _empty_profile())
    data = _load_json(PROFILE, _empty_profile())
    path = args.key.split(".")
    if not all(p for p in path):
        _die("empty segment in key", 3)
    _plant(data, path, _coerce(args.value))
    data["updated_at"] = _now()
    _write_json(PROFILE, data)
    print(json.dumps({"updated": args.key, "value": _dive(data, path)}))
    return 0


def cmd_save_audit(args: argparse.Namespace) -> int:
    src = Path(args.audit_file).expanduser().resolve()
    if not src.exists():
        _die(f"audit file not found: {src}", 4)
    blob = _load_json(src, None)
    if not isinstance(blob, dict):
        _die("audit file is not a JSON object", 3)

    platform = blob.get("platform")
    if platform not in ("meta", "google", "tiktok"):
        _die(f"audit JSON missing/invalid platform (got {platform!r})", 3)

    # Microsecond precision so two saves in the same second don't collide.
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%d%H%M%S%f")
    fname = f"{platform}-{ts}.json"
    HISTORY.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, HISTORY / fname)

    # critical_count / quick_wins_count are NOT canonical fields in
    # audit-output-schema.json — derive them from the arrays if present, but
    # honor an explicit top-level field if the audit producer set one
    # (legacy compatibility).
    def _count(field: str, array_field: str) -> int | None:
        v = blob.get(field)
        if isinstance(v, int):
            return v
        arr = blob.get(array_field)
        return len(arr) if isinstance(arr, list) else None

    idx = _load_json(INDEX, _empty_index())
    idx.setdefault("audits", []).append({
        "platform": platform,
        # Prefer the audit's own generated_at so the history reflects when the
        # audit actually ran, not when the user happened to save it.
        "timestamp": blob.get("generated_at") or _now(),
        "health_score": blob.get("health_score"),
        "grade": blob.get("grade"),
        "data_source": blob.get("data_source"),
        "critical_count":   _count("critical_count",   "critical_issues"),
        "quick_wins_count": _count("quick_wins_count", "quick_wins"),
        "file": fname,
    })
    _write_json(INDEX, idx)
    print(json.dumps({"saved": fname, "platform": platform}))
    return 0


def _check_id(item: dict[str, Any]) -> str:
    return str(item.get("id") or item.get("check_id") or item.get("title") or "")


def cmd_compare(args: argparse.Namespace) -> int:
    platform = args.platform
    if platform not in ("meta", "google", "tiktok"):
        _die("platform must be meta|google|tiktok", 3)
    idx = _load_json(INDEX, _empty_index())
    entries = [a for a in idx.get("audits", []) if a.get("platform") == platform]
    if len(entries) < 2:
        print(json.dumps({"comparable": False, "reason": f"need 2 audits for {platform}, have {len(entries)}"}))
        return 0

    latest, prev = entries[-1], entries[-2]
    latest_blob = _load_json(HISTORY / latest["file"], {})
    prev_blob   = _load_json(HISTORY / prev["file"], {})

    def issue_set(blob: dict[str, Any]) -> set[str]:
        ids: set[str] = set()
        for bucket in ("critical_issues", "issues", "checks"):
            for item in blob.get(bucket, []) or []:
                if isinstance(item, dict):
                    status = (item.get("status") or item.get("result") or "").upper()
                    if status in ("FAIL", "WARNING") or bucket == "critical_issues":
                        cid = _check_id(item)
                        if cid:
                            ids.add(cid)
        return ids

    latest_ids = issue_set(latest_blob)
    prev_ids = issue_set(prev_blob)

    score_l = latest.get("health_score")
    score_p = prev.get("health_score")
    delta = None
    if isinstance(score_l, (int, float)) and isinstance(score_p, (int, float)):
        delta = score_l - score_p

    print(json.dumps({
        "comparable": True,
        "platform": platform,
        "score_delta": delta,
        "grade_change": {"from": prev.get("grade"), "to": latest.get("grade")},
        "new_issues":      sorted(latest_ids - prev_ids),
        "resolved_issues": sorted(prev_ids - latest_ids),
        "latest_file": latest["file"],
        "prev_file": prev["file"],
    }, indent=2))
    return 0


def cmd_reset(args: argparse.Namespace) -> int:
    if not args.yes:
        # The agent should call AskUserQuestion BEFORE invoking with --yes.
        # Direct CLI users get a single-line confirmation prompt.
        if sys.stdin.isatty():
            print(f"This wipes {ROOT}. Type 'yes' to confirm: ", end="", flush=True)
            try:
                answer = input().strip().lower()
            except (KeyboardInterrupt, EOFError):
                answer = ""
            if answer != "yes":
                print(json.dumps({"reset": False, "reason": "cancelled"}))
                return 0
        else:
            _die("reset requires --yes when stdin is not a tty", 3)
    if ROOT.exists():
        shutil.rmtree(ROOT)
    print(json.dumps({"reset": True, "path": str(ROOT)}))
    return 0


# --------------------------------------------------------------------------- #
# CLI                                                                         #
# --------------------------------------------------------------------------- #

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="profile.py",
        description="claude-ads profile + audit-history utility (pure stdlib).",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="Create empty profile if missing (idempotent).").set_defaults(fn=cmd_init)

    g = sub.add_parser("get", help="Print profile or a sub-key.")
    g.add_argument("--key", help="Dot-path, e.g. context.industry")
    g.set_defaults(fn=cmd_get)

    s = sub.add_parser("set", help="Update a field (auto-creates intermediates).")
    s.add_argument("key")
    s.add_argument("value")
    s.set_defaults(fn=cmd_set)

    sa = sub.add_parser("save-audit", help="Copy audit JSON into history/ and append index.")
    sa.add_argument("audit_file")
    sa.set_defaults(fn=cmd_save_audit)

    c = sub.add_parser("compare", help="Diff most-recent vs previous audit for a platform.")
    c.add_argument("platform", choices=["meta", "google", "tiktok"])
    c.set_defaults(fn=cmd_compare)

    r = sub.add_parser("reset", help="Wipe ~/.claude-ads/ (asks unless --yes).")
    r.add_argument("--yes", action="store_true")
    r.set_defaults(fn=cmd_reset)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.fn(args)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        _die(f"unexpected: {exc!r}", 4)
        return 4


if __name__ == "__main__":
    sys.exit(main())
