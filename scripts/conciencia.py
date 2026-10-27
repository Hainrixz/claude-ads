#!/usr/bin/env python3
# Portions Copyright (c) 2026 Enrique Rocha (@soyenriquerocha) - see LICENSE for original authors
# SPDX-License-Identifier: MIT
# id: er-fd4fa55b
"""claude-ads campaign awareness ("conciencia de campaña") — pure-stdlib CLI
for ~/.claude-ads/conciencia/<platform>-<campaign_id>.json.

Platforms only see clicks and messages. Whether a WhatsApp / form / call
campaign actually closed customers is known only by the user. This script
stores those dated business outcomes, keeps track of what Claude knows and
does NOT know, and cross-references platform metrics with user reports to
derive the real success rate of the campaign. Unreported values stay null —
a ratio is only computed from check-ins where both sides were reported.

Subcommands
-----------
  register --platform --campaign-id --name --objective --channel
           [--ticket-value N] [--currency X] [--started-at YYYY-MM-DD] [--every 7]
                              Create the awareness file (idempotent).
  checkin <key> --json '<payload>'
                              Append a dated check-in, reschedule next one.
  due                         List active campaigns whose check-in is overdue.
  show <key>                  Record + derived metrics as JSON.
  list                        Every tracked campaign with status.
  render <key> [--out PATH]   Write the human-readable markdown file.
  know <key> --fact TEXT [--source user]
                              Record a known fact with its source.
  snooze <key> [--days 1]     Push the next check-in forward.
  close <key>                 Mark campaign closed (keeps the file).

<key> is "<platform>-<campaign_id>", e.g. meta-120210000000001.

Exit codes
----------
  0  success
  2  campaign not found
  3  validation / argument error
  4  IO error

All commands emit JSON on stdout. Errors print a single JSON line to stderr.
This script intentionally has zero non-stdlib imports.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

# --------------------------------------------------------------------------- #
# Paths                                                                       #
# --------------------------------------------------------------------------- #

HOME = Path(os.environ.get("HOME") or os.path.expanduser("~"))
ROOT = HOME / ".claude-ads"
CONCIENCIA = ROOT / "conciencia"

SCHEMA_VERSION = "1.0"
PLATFORMS = ("meta", "google", "tiktok")
OBJECTIVES = ("leads", "messages", "calls", "forms", "sales")
CHANNELS = ("whatsapp", "messenger", "instagram_dm", "form", "call", "landing", "pixel_purchase")
SOURCES = ("audit", "user", "api", "mcp", "export")
METRIC_SOURCES = (None, "mcp", "api", "export", "audit", "user")

PLATFORM_FIELDS = {"spend": float, "clicks": int, "messages": int, "leads": int}
USER_FIELDS = {"conversations": int, "qualified": int, "closed": int, "revenue": float, "junk": int}

# Business outcome → what Claude doesn't know until the user reports it.
UNKNOWN_LABELS = {
    "conversations": "Conversaciones reales recibidas",
    "qualified": "Leads calificados",
    "closed": "Clientes cerrados (tasa de cierre)",
    "revenue": "Ingreso generado",
    "junk": "Calidad de los leads (% basura)",
}

KEY_RE = re.compile(r"^(meta|google|tiktok)-[A-Za-z0-9_.-]+$")


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #

def _utcnow() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0)


def _iso(d: _dt.datetime) -> str:
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso(s: str | None) -> _dt.datetime | None:
    if not s:
        return None
    try:
        return _dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)
    except ValueError:
        return None


def _die(msg: str, code: int = 3) -> None:
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(code)


def _load_json(p: Path) -> Any:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        _die(f"{p}: invalid JSON ({e})", 4)


def _write_json(p: Path, data: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(p)


def _path(key: str) -> Path:
    if not KEY_RE.match(key):
        _die(f"invalid key {key!r} (expected <platform>-<campaign_id>)", 3)
    return CONCIENCIA / f"{key}.json"


def _load(key: str) -> dict[str, Any]:
    p = _path(key)
    if not p.exists():
        print(json.dumps({"missing": True, "key": key}), file=sys.stderr)
        sys.exit(2)
    return _load_json(p)


def _save(key: str, rec: dict[str, Any]) -> None:
    rec["updated_at"] = _iso(_utcnow())
    rec["unknowns"] = _unknowns(rec)
    _write_json(_path(key), rec)


def _key_of(rec: dict[str, Any]) -> str:
    c = rec["campaign"]
    return f"{c['platform']}-{c['campaign_id']}"


def _clean_number(name: str, value: Any, kind: type) -> int | float | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        _die(f"{name}: expected a number, got a boolean", 3)
    try:
        num = kind(value)
    except (TypeError, ValueError):
        _die(f"{name}: expected a number, got {value!r}", 3)
    if kind is int and float(value) != num:
        _die(f"{name}: expected a whole number, got {value!r}", 3)
    if num < 0:
        _die(f"{name}: must be >= 0", 3)
    return num


def _clean_block(name: str, raw: Any, fields: dict[str, type]) -> dict[str, Any]:
    raw = raw or {}
    if not isinstance(raw, dict):
        _die(f"{name}: expected an object", 3)
    extra = set(raw) - set(fields) - ({"notes"} if name == "user_reported" else set())
    if extra:
        _die(f"{name}: unknown fields {sorted(extra)}", 3)
    out = {f: _clean_number(f"{name}.{f}", raw.get(f), kind) for f, kind in fields.items()}
    if name == "user_reported":
        notes = raw.get("notes")
        out["notes"] = str(notes) if notes not in (None, "") else None
    return out


def _unknowns(rec: dict[str, Any]) -> list[str]:
    if rec["campaign"]["tracking_mode"] == "pixel":
        return []
    reported = {
        f for c in rec["checkins"] for f, v in c["user_reported"].items() if v is not None
    }
    out = [label for f, label in UNKNOWN_LABELS.items() if f not in reported]
    # Revenue is covered by an estimate when the ticket value is known.
    if "revenue" not in reported and rec["campaign"].get("ticket_value") is not None:
        out.remove(UNKNOWN_LABELS["revenue"])
    if not any(c["platform_metrics"].get("spend") is not None for c in rec["checkins"]):
        out.append("Métricas de plataforma del periodo (gasto, clics, mensajes)")
    return out


# --------------------------------------------------------------------------- #
# Metrics                                                                     #
# --------------------------------------------------------------------------- #

def _val(c: dict[str, Any], field: str) -> Any:
    if field in PLATFORM_FIELDS:
        return c["platform_metrics"].get(field)
    return c["user_reported"].get(field)


def _ratio(checkins: list[dict[str, Any]], num: str, den: str, digits: int) -> dict[str, Any]:
    """Sum num/den only over check-ins where BOTH were reported."""
    pairs = [(_val(c, num), _val(c, den)) for c in checkins]
    pairs = [(n, d) for n, d in pairs if n is not None and d is not None]
    total_den = sum(d for _, d in pairs)
    if not pairs or total_den == 0:
        return {"value": None, "checkins": len(pairs)}
    return {"value": round(sum(n for n, _ in pairs) / total_den, digits), "checkins": len(pairs)}


def _metrics(checkins: list[dict[str, Any]], ticket_value: float | None) -> dict[str, Any]:
    m = {
        "click_to_message_rate": _ratio(checkins, "messages", "clicks", 4),
        "platform_vs_real":      _ratio(checkins, "conversations", "messages", 4),
        "qualification_rate":    _ratio(checkins, "qualified", "conversations", 4),
        "close_rate":            _ratio(checkins, "closed", "conversations", 4),
        "close_rate_qualified":  _ratio(checkins, "closed", "qualified", 4),
        "junk_rate":             _ratio(checkins, "junk", "conversations", 4),
        "cost_per_conversation": _ratio(checkins, "spend", "conversations", 2),
        "cost_per_close":        _ratio(checkins, "spend", "closed", 2),
        "real_roas":             _ratio(checkins, "revenue", "spend", 2),
        "estimated_roas":        {"value": None, "checkins": 0},
    }
    if ticket_value is not None:
        pairs = [(_val(c, "closed"), _val(c, "spend")) for c in checkins]
        pairs = [(n, s) for n, s in pairs if n is not None and s]
        if pairs:
            m["estimated_roas"] = {
                "value": round(sum(n for n, _ in pairs) * ticket_value / sum(s for _, s in pairs), 2),
                "checkins": len(pairs),
            }
    totals: dict[str, Any] = {}
    for f in (*PLATFORM_FIELDS, *USER_FIELDS):
        vals = [_val(c, f) for c in checkins if _val(c, f) is not None]
        totals[f] = round(sum(vals), 2) if vals else None
    m["totals"] = totals
    return m


def _derive(rec: dict[str, Any]) -> dict[str, Any]:
    cks = rec["checkins"]
    tv = rec["campaign"].get("ticket_value")
    latest = _metrics(cks[-1:], tv) if cks else None
    previous = _metrics(cks[-2:-1], tv) if len(cks) >= 2 else None
    trend = None
    if latest and previous:
        trend = {}
        for k in ("close_rate", "junk_rate", "cost_per_close"):
            a, b = latest[k]["value"], previous[k]["value"]
            trend[k] = round(a - b, 4) if a is not None and b is not None else None
    return {"cumulative": _metrics(cks, tv), "latest": latest, "previous": previous, "trend": trend}


# --------------------------------------------------------------------------- #
# Subcommands                                                                 #
# --------------------------------------------------------------------------- #

def cmd_register(args: argparse.Namespace) -> int:
    key = f"{args.platform}-{args.campaign_id}"
    p = _path(key)
    if p.exists():
        print(json.dumps({"created": False, "key": key, "path": str(p)}))
        return 0
    if args.started_at:
        try:
            _dt.date.fromisoformat(args.started_at)
        except ValueError:
            _die("--started-at must be YYYY-MM-DD", 3)
    now = _utcnow()
    rec = {
        "version": SCHEMA_VERSION,
        "created_at": _iso(now),
        "updated_at": _iso(now),
        "campaign": {
            "platform": args.platform,
            "campaign_id": args.campaign_id,
            "name": args.name,
            "objective": args.objective,
            "conversion_channel": args.channel,
            "tracking_mode": "pixel" if args.channel == "pixel_purchase" else "offline",
            "ticket_value": args.ticket_value,
            "currency": args.currency,
            "started_at": args.started_at,
        },
        "knowns": [],
        "unknowns": [],
        "checkins": [],
        "checkin_every_days": args.every,
        "next_checkin_at": _iso(now + _dt.timedelta(days=args.every)),
        "status": "active",
    }
    _save(key, rec)
    print(json.dumps({"created": True, "key": key, "path": str(p)}))
    return 0


def cmd_checkin(args: argparse.Namespace) -> int:
    rec = _load(args.key)
    try:
        payload = json.loads(args.json)
    except json.JSONDecodeError as e:
        _die(f"--json is not valid JSON ({e})", 3)
    if not isinstance(payload, dict):
        _die("--json must be an object", 3)
    extra = set(payload) - {"period_from", "period_to", "source_of_platform_metrics",
                            "platform_metrics", "user_reported"}
    if extra:
        _die(f"unknown check-in fields {sorted(extra)}", 3)
    for f in ("period_from", "period_to"):
        if payload.get(f):
            try:
                _dt.date.fromisoformat(payload[f])
            except ValueError:
                _die(f"{f} must be YYYY-MM-DD", 3)
    src = payload.get("source_of_platform_metrics")
    if src not in METRIC_SOURCES:
        _die(f"source_of_platform_metrics must be one of {list(METRIC_SOURCES)}", 3)

    now = _utcnow()
    rec["checkins"].append({
        "date": _iso(now),
        "period_from": payload.get("period_from"),
        "period_to": payload.get("period_to"),
        "source_of_platform_metrics": src,
        "platform_metrics": _clean_block("platform_metrics", payload.get("platform_metrics"), PLATFORM_FIELDS),
        "user_reported": _clean_block("user_reported", payload.get("user_reported"), USER_FIELDS),
    })
    rec["next_checkin_at"] = _iso(now + _dt.timedelta(days=rec["checkin_every_days"]))
    if rec["status"] == "paused":
        rec["status"] = "active"
    _save(args.key, rec)
    print(json.dumps({
        "key": args.key,
        "checkins": len(rec["checkins"]),
        "next_checkin_at": rec["next_checkin_at"],
        "unknowns": rec["unknowns"],
    }, ensure_ascii=False))
    return 0


def _all_records() -> list[dict[str, Any]]:
    if not CONCIENCIA.exists():
        return []
    return [_load_json(p) for p in sorted(CONCIENCIA.glob("*.json"))]


def cmd_due(args: argparse.Namespace) -> int:
    now = _utcnow()
    due = []
    for rec in _all_records():
        if rec.get("status") != "active" or rec["campaign"].get("tracking_mode") != "offline":
            continue
        when = _parse_iso(rec.get("next_checkin_at"))
        if when is not None and when <= now:
            due.append({
                "key": _key_of(rec),
                "name": rec["campaign"]["name"],
                "platform": rec["campaign"]["platform"],
                "channel": rec["campaign"]["conversion_channel"],
                "next_checkin_at": rec["next_checkin_at"],
                "days_overdue": (now - when).days,
                "last_checkin_at": rec["checkins"][-1]["date"] if rec["checkins"] else None,
            })
    print(json.dumps({"due": due}, ensure_ascii=False, indent=2))
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    rec = _load(args.key)
    print(json.dumps({**rec, "metrics": _derive(rec)}, ensure_ascii=False, indent=2))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    rows = []
    for rec in _all_records():
        close = _derive(rec)["cumulative"]["close_rate"]
        rows.append({
            "key": _key_of(rec),
            "name": rec["campaign"]["name"],
            "status": rec["status"],
            "tracking_mode": rec["campaign"]["tracking_mode"],
            "checkins": len(rec["checkins"]),
            "close_rate": close["value"],
            "next_checkin_at": rec.get("next_checkin_at"),
        })
    print(json.dumps({"campaigns": rows}, ensure_ascii=False, indent=2))
    return 0


def cmd_know(args: argparse.Namespace) -> int:
    rec = _load(args.key)
    rec["knowns"].append({"fact": args.fact, "source": args.source, "date": _iso(_utcnow())})
    _save(args.key, rec)
    print(json.dumps({"key": args.key, "knowns": len(rec["knowns"])}))
    return 0


def cmd_snooze(args: argparse.Namespace) -> int:
    rec = _load(args.key)
    rec["next_checkin_at"] = _iso(_utcnow() + _dt.timedelta(days=args.days))
    _save(args.key, rec)
    print(json.dumps({"key": args.key, "next_checkin_at": rec["next_checkin_at"]}))
    return 0


def cmd_close(args: argparse.Namespace) -> int:
    rec = _load(args.key)
    rec["status"] = "closed"
    rec["next_checkin_at"] = None
    _save(args.key, rec)
    print(json.dumps({"key": args.key, "status": "closed"}))
    return 0


# --------------------------------------------------------------------------- #
# Markdown render                                                             #
# --------------------------------------------------------------------------- #

METRIC_LABELS = {
    "close_rate":            ("Tasa de cierre (cerrados / conversaciones)", "pct", "clientes cerrados y conversaciones reales"),
    "close_rate_qualified":  ("Cierre sobre calificados", "pct", "clientes cerrados y leads calificados"),
    "qualification_rate":    ("Leads calificados / conversaciones", "pct", "leads calificados"),
    "junk_rate":             ("% basura", "pct", "cuántos contactos fueron basura"),
    "platform_vs_real":      ("Conversaciones reales / mensajes que cuenta la plataforma", "pct", "conversaciones reales y mensajes de plataforma"),
    "click_to_message_rate": ("Clic → mensaje", "pct", "clics y mensajes de plataforma"),
    "cost_per_conversation": ("Costo por conversación real", "money", "gasto y conversaciones reales"),
    "cost_per_close":        ("Costo por cliente cerrado", "money", "gasto y clientes cerrados"),
    "real_roas":             ("ROAS real (ingreso / gasto)", "x", "ingreso generado y gasto"),
    "estimated_roas":        ("ROAS estimado (cerrados × ticket / gasto)", "x", "ticket promedio, cerrados y gasto"),
}


def _fmt(value: Any, kind: str, currency: str | None) -> str:
    if value is None:
        return "N/A"
    if kind == "pct":
        return f"{value * 100:.1f} %"
    if kind == "money":
        return f"{value:,.2f} {currency or ''}".strip()
    if kind == "x":
        return f"{value:.2f}x"
    return str(value)


def _render(rec: dict[str, Any]) -> str:
    c = rec["campaign"]
    d = _derive(rec)
    cur = c.get("currency")
    cum = d["cumulative"]
    lines = [
        f"# Conciencia de campaña — {c['name']}",
        "",
        f"- **Plataforma:** {c['platform']} · **ID:** `{c['campaign_id']}`",
        f"- **Objetivo:** {c['objective']} · **Canal de conversión:** {c['conversion_channel']}",
        f"- **Ticket promedio:** {_fmt(c.get('ticket_value'), 'money', cur)}",
        f"- **Estado:** {rec['status']} · **Check-ins:** {len(rec['checkins'])}"
        f" · **Próximo check-in:** {rec.get('next_checkin_at') or '—'}",
        f"- **Actualizado:** {rec['updated_at']}",
        "",
    ]
    if c["tracking_mode"] == "pixel":
        lines += [
            "> Esta campaña vende con píxel de compra: la plataforma ya ve la venta.",
            "> La conciencia es opcional aquí.",
            "",
        ]

    known = [(k, v) for k, v in cum.items() if k != "totals" and v["value"] is not None]
    missing = [(k, v) for k, v in cum.items() if k != "totals" and v["value"] is None]

    lines += ["## Lo que sé", ""]
    if known:
        lines += ["| Métrica | Valor acumulado | Check-ins con dato |", "|---|---|---|"]
        for k, v in known:
            label, kind, _ = METRIC_LABELS[k]
            lines.append(f"| {label} | {_fmt(v['value'], kind, cur)} | {v['checkins']} |")
        lines.append("")
    t = cum["totals"]
    total_bits = [f"{k}: {v}" for k, v in t.items() if v is not None]
    if total_bits:
        lines += ["**Totales reportados:** " + " · ".join(total_bits), ""]
    for f in rec["knowns"]:
        lines.append(f"- {f['fact']} _(fuente: {f['source']}, {f['date'][:10]})_")
    if not known and not total_bits and not rec["knowns"]:
        lines.append("Todavía nada confirmado. Falta el primer check-in.")
    lines.append("")

    unknown_lines = [f"- {u}" for u in rec["unknowns"]]
    for k, _ in missing:
        label, _, needs = METRIC_LABELS[k]
        # The estimate is redundant once real revenue is reported.
        if k == "estimated_roas" and cum["real_roas"]["value"] is not None:
            continue
        unknown_lines.append(f"- {label}: N/A — falta {needs}.")
    lines += ["## Lo que no sé", "", *(unknown_lines or ["- Nada pendiente por ahora."]), ""]

    if d["trend"]:
        tr = d["trend"]
        lines += ["## Tendencia vs check-in anterior", ""]
        for k in ("close_rate", "junk_rate", "cost_per_close"):
            label, kind, _ = METRIC_LABELS[k]
            v = tr[k]
            if v is None:
                lines.append(f"- {label}: N/A")
            else:
                sign = "+" if v > 0 else ""
                shown = f"{sign}{v * 100:.1f} pts" if kind == "pct" else f"{sign}{v:,.2f} {cur or ''}".strip()
                lines.append(f"- {label}: {shown}")
        lines.append("")

    lines += ["## Historial de check-ins", ""]
    if rec["checkins"]:
        lines += [
            "| Fecha | Periodo | Gasto | Clics | Mensajes | Conversaciones | Calificados | Cerrados | Ingreso | Basura | Notas |",
            "|---|---|---|---|---|---|---|---|---|---|---|",
        ]
        for ck in rec["checkins"]:
            pm, ur = ck["platform_metrics"], ck["user_reported"]
            period = f"{ck.get('period_from') or '?'} → {ck.get('period_to') or '?'}"
            cells = [pm["spend"], pm["clicks"], pm["messages"], ur["conversations"],
                     ur["qualified"], ur["closed"], ur["revenue"], ur["junk"]]
            row = " | ".join("N/A" if v is None else str(v) for v in cells)
            lines.append(f"| {ck['date'][:10]} | {period} | {row} | {ur.get('notes') or ''} |")
    else:
        lines.append("Sin check-ins todavía.")
    lines += [
        "",
        "---",
        "Generado por `/ads conciencia`. Fuente de verdad: "
        f"`~/.claude-ads/conciencia/{_key_of(rec)}.json`. N/A = no reportado, nunca se asume.",
        "",
    ]
    return "\n".join(lines)


def cmd_render(args: argparse.Namespace) -> int:
    rec = _load(args.key)
    out = Path(args.out or "conciencia-de-campana.md").expanduser()
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(_render(rec), encoding="utf-8")
    except OSError as e:
        _die(f"could not write {out}: {e}", 4)
    print(json.dumps({"key": args.key, "written": str(out.resolve())}))
    return 0


# --------------------------------------------------------------------------- #
# CLI                                                                         #
# --------------------------------------------------------------------------- #

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(epilog='Hecho por Enrique Rocha (@soyenriquerocha) · tododeia.com',
        prog="conciencia.py",
        description="claude-ads campaign awareness: business outcomes the platforms can't see (pure stdlib).",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("register", help="Create the awareness file for a campaign (idempotent).")
    r.add_argument("--platform", required=True, choices=PLATFORMS)
    r.add_argument("--campaign-id", required=True)
    r.add_argument("--name", required=True)
    r.add_argument("--objective", required=True, choices=OBJECTIVES)
    r.add_argument("--channel", required=True, choices=CHANNELS)
    r.add_argument("--ticket-value", type=float, default=None)
    r.add_argument("--currency", default=None)
    r.add_argument("--started-at", default=None, help="YYYY-MM-DD")
    r.add_argument("--every", type=int, default=7, help="Days between check-ins (default 7).")
    r.set_defaults(fn=cmd_register)

    c = sub.add_parser("checkin", help="Append a dated check-in.")
    c.add_argument("key")
    c.add_argument("--json", required=True, help="Check-in payload (see conciencia-schema.json).")
    c.set_defaults(fn=cmd_checkin)

    sub.add_parser("due", help="List campaigns with an overdue check-in.").set_defaults(fn=cmd_due)

    s = sub.add_parser("show", help="Record + derived metrics.")
    s.add_argument("key")
    s.set_defaults(fn=cmd_show)

    sub.add_parser("list", help="All tracked campaigns.").set_defaults(fn=cmd_list)

    rd = sub.add_parser("render", help="Write the markdown awareness file.")
    rd.add_argument("key")
    rd.add_argument("--out", default=None, help="Default: ./conciencia-de-campana.md")
    rd.set_defaults(fn=cmd_render)

    k = sub.add_parser("know", help="Record a known fact with its source.")
    k.add_argument("key")
    k.add_argument("--fact", required=True)
    k.add_argument("--source", default="user", choices=SOURCES)
    k.set_defaults(fn=cmd_know)

    sn = sub.add_parser("snooze", help="Push the next check-in forward.")
    sn.add_argument("key")
    sn.add_argument("--days", type=int, default=1)
    sn.set_defaults(fn=cmd_snooze)

    cl = sub.add_parser("close", help="Mark campaign closed (keeps the file).")
    cl.add_argument("key")
    cl.set_defaults(fn=cmd_close)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "every", 1) < 1 or getattr(args, "days", 1) < 1:
        _die("--every / --days must be >= 1", 3)
    if getattr(args, "ticket_value", None) is not None and args.ticket_value < 0:
        _die("--ticket-value must be >= 0", 3)
    try:
        return args.fn(args)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        _die(f"unexpected: {exc!r}", 4)
        return 4


if __name__ == "__main__":
    sys.exit(main())
